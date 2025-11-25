# predict_service.py - service layer, không khai báo router ở đây
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import io
from config import *

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

gender_labels = ['Male', 'Female']

class FaceGender(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = models.resnet18(weights=None)
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, 2)
    def forward(self, x):
        return self.backbone(x)

class FaceAge(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = models.resnet18(weights=None)
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, 1)
    def forward(self, x):
        return self.backbone(x)

# Shared model instances
try:
    model_age = FaceAge().to(device)
    model_age.load_state_dict(torch.load(AGE_MODEL, map_location=device))
    model_age.eval()
    model_gender = FaceGender().to(device)
    model_gender.load_state_dict(torch.load(GENDER_MODEL, map_location=device))
    model_gender.eval()
except Exception as e:
    model_age = None
    model_gender = None
    print(f"Error loading models: {e}")

# Service function giống face_query_service
async def predict_service(file):
    if model_age is None or model_gender is None:
        return {"error": "Model not loaded", "status_code": 500}
    # Đọc file bytes
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        return {"error": "Invalid image file", "status_code": 400}
    # Dự đoán
    img_tensor = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        age_pred = max(0, int(model_age(img_tensor).item()))
        gender_logits = model_gender(img_tensor)
        gender_pred = torch.argmax(gender_logits, dim=1).item()
    return {
        "pred_age": age_pred,
        "pred_gender": gender_labels[gender_pred]
    }
