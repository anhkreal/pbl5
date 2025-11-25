import torch
import numpy as np
import cv2
from pathlib import Path

EMOTION_CLASSES = {0: "Neutral", 1: "Happy", 2: "Sad", 3: "Surprise", 4: "Fear", 5: "Disgust", 6: "Anger", 7: "Contempt"}


class EmoNetWrapper:
    def __init__(self, model_path: str = 'model/emonet_8.pth'):
        self.model_path = Path(model_path)
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.net = None
        self._load()

    def _load(self):
        if not self.model_path.exists():
            # model missing — leave net as None
            print(f"EmoNet model not found at {self.model_path}; emotion prediction disabled.")
            return
        try:
            state = torch.load(str(self.model_path), map_location='cpu')
            # support DataParallel checkpoints
            state = {k.replace('module.', ''): v for k, v in state.items()}
            from emonet.models import EmoNet
            net = EmoNet(n_expression=8)
            net.load_state_dict(state, strict=False)
            net.to(self.device)
            net.eval()
            self.net = net
        except Exception as e:
            import traceback
            print("Failed to load EmoNet model — emotion prediction disabled.")
            traceback.print_exc()
            print(f"EmoNet load exception: {e}")
            self.net = None

    def predict_from_image_bgr(self, img_bgr: np.ndarray):
        """Predict emotion from BGR image (numpy). Returns (label, prob) or (None, None) on error."""
        if self.net is None:
            return None, None
        try:
            # ensure 3 channels
            if img_bgr.ndim == 2:
                img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_GRAY2BGR)
            if img_bgr.shape[2] > 3:
                img_bgr = img_bgr[:, :, :3]
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            img_resized = cv2.resize(img_rgb, (256, 256))
            tensor = torch.from_numpy(img_resized.astype(np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0).to(self.device)
            with torch.no_grad():
                out = self.net(tensor)
                expr = out.get('expression')
                if expr is None:
                    return None, None
                probs = torch.nn.functional.softmax(expr, dim=1)
                pred = int(torch.argmax(probs, dim=1).cpu().item())
                prob = float(probs[0, pred].cpu().item())
                return EMOTION_CLASSES.get(pred, str(pred)), prob
        except Exception:
            return None, None


# Singleton wrapper
_EMO_WRAPPER = None


def get_emonet_wrapper():
    global _EMO_WRAPPER
    if _EMO_WRAPPER is None:
        _EMO_WRAPPER = EmoNetWrapper()
    return _EMO_WRAPPER


def predict_emotion_from_bytes(image_bytes: bytes):
    wrapper = get_emonet_wrapper()
    if wrapper.net is None:
        # Return a consistent dict so callers can always include the field in JSON
        return {"emotion": None, "prob": None}
    try:
        buf = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        if img is None:
            return {"emotion": None, "prob": None}
        label, prob = wrapper.predict_from_image_bgr(img)
        if label is None:
            return {"emotion": None, "prob": None}
        return {"emotion": label, "prob": prob}
    except Exception:
        return {"emotion": None, "prob": None}
