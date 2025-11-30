import AdminLayout from '../../layouts/AdminLayout';
import AdminPinModal from '../../components/AdminPinModal';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchEmployees, shiftEmployee, resetEmployee, deleteEmployee, createEmployee, Employee, shiftEmployeeByUsername, resignEmployeeByUsername, addUserAndAccount } from '../../api/employees';
import { verifyPin } from '../../api/pin';

export default function Employees(){
  const [q,setQ]=useState('');
  const [employees,setEmployees]=useState<Employee[]>([]);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  const [modalAction,setModalAction]=useState<{type:'shift'|'reset'|'delete'|'add',id:number,username?:string}|null>(null);
  const [showAdd,setShowAdd]=useState(false);
  const [newEmp,setNewEmp]=useState<{name:string,username:string,age:string,address:string,phone:string,shift:'day'|'night'}>({name:'',username:'',age:'',address:'',phone:'',shift:'day'});

  const list=employees;
  const navigate = useNavigate();

  useEffect(()=>{
    let ignore=false;
    (async()=>{
      setLoading(true); setError('');
      try{
        const data = await fetchEmployees(q || undefined);
        if(!ignore) setEmployees(data);
      }catch(e:any){ setError(e.message); }finally{ if(!ignore) setLoading(false); }
    })();
    return ()=>{ignore=true;}
  },[q]);

  const performAction = async (pin: string) => {
    if(!modalAction) return;
    const trimmed = String(pin ?? '').trim();
    console.debug('[Employees] performAction pin raw:', pin, 'trimmed:', trimmed);
    const ok = await verifyPin(trimmed);
    if(!ok){ alert('PIN sai'); return; }
    if(modalAction.type==='shift' && modalAction.username) {
      const emp = employees.find(x => x.username === modalAction.username);
      if (!emp) { alert('Không tìm thấy nhân viên!'); return; }
      await shiftEmployeeByUsername(modalAction.username, emp.shift);
      alert('Đã đổi ca thành công!');
    }
    if(modalAction.type==='delete' && modalAction.username) {
      await resignEmployeeByUsername(modalAction.username);
      setEmployees(e=>e.filter(x=>x.username!==modalAction.username));
      alert('Đã cho nghỉ việc!');
    }
    if(modalAction.type==='reset') await resetEmployee(modalAction.id);
    if(modalAction.type==='add'){
      if (!newEmp.username.trim()) {
        alert('Username là bắt buộc!');
        return;
      }
      await addUserAndAccount({
        username: newEmp.username.trim(),
        full_name: newEmp.name?.trim() || undefined,
        age: newEmp.age?.trim() ? Number(newEmp.age) : undefined,
        address: newEmp.address?.trim() || undefined,
        phone: newEmp.phone?.trim() || undefined,
        shift: newEmp.shift || 'day',
      });
      const data=await fetchEmployees(); setEmployees(data);
    }
    setModalAction(null); setShowAdd(false);
  };

  return (
    <AdminLayout>
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:18}}>
        <h1 style={{margin:0}}>Nhân viên</h1>
        <button onClick={()=>{setShowAdd(true);setNewEmp({name:'',username:'',age:'',address:'',phone:'',shift:'day'});}} style={{padding:'8px 16px',borderRadius:4,border:'none',background:'#3498db',color:'#fff',fontWeight:600,cursor:'pointer'}}>+ Thêm nhân viên mới</button>
      </div>
      <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Tìm tên hoặc nhập ID để xem chi tiết" style={{padding:8,border:'1px solid #ccc',borderRadius:4,marginBottom:14}}/>
      {loading && <div style={{padding:10}}>Đang tải...</div>}
      {error && <div style={{padding:10,color:'red'}}>{error}</div>}
      <div style={{background:'#fff',borderRadius:8,overflowX:'auto'}}>
        <table style={{width:'100%',borderCollapse:'collapse'}}>
          <thead>
            <tr style={{background:'#f5f5f5'}}>
              <th style={th}>STT</th>
              <th style={th}>Avatar</th>
              <th style={th}>Tên</th>
              <th style={th}>Ca</th>
              <th style={th}>Trạng thái</th>
              <th style={th}>Hành động</th>
            </tr>
          </thead>
          <tbody>
            {list.map((e,i)=>(
              <tr key={e.id} style={{borderTop:'1px solid #ecf0f1'}}>
                <td style={td}>{i+1}</td>
                <td style={td}>
                  {e.avatar_base64
                    ? (
                        <img
                          src={
                            e.avatar_base64.startsWith('data:image')
                              ? e.avatar_base64
                              : `data:image/png;base64,${e.avatar_base64}`
                          }
                          style={{ width: 40, height: 40, borderRadius: 4 }}
                        />
                      )
                    : <div style={{ width: 40, height: 40, background: '#ecf0f1', borderRadius: 4 }} />}
                </td>
                <td style={td}><button onClick={() => navigate('/admin/employeedetail?username=' + encodeURIComponent(String(e.username)))} style={{ background: 'transparent', border: 'none', padding: 0, color: '#3498db', cursor: 'pointer' }}>{e.fullName}</button></td>
                <td style={td}>{e.shift==='day'?'Ngày':'Đêm'}</td>
                <td style={td}><span style={badge(e.status==='working'?'#2ecc71':'#7f8c8d')}>{e.status==='working'?'Đang làm':'Đã nghỉ'}</span></td>
                <td style={td}>
                  <button onClick={()=>setModalAction({type:'shift',id:e.id,username:e.username})} style={{marginRight:8,padding:'4px 10px',borderRadius:4,border:'1px solid #ccc',background:'#f5f6fa',cursor:'pointer'}}>Đổi ca</button>
                  <button onClick={()=>setModalAction({type:'delete',id:e.id,username:e.username})} style={{padding:'4px 10px',borderRadius:4,border:'1px solid #e74c3c',background:'#fff',color:'#e74c3c',cursor:'pointer'}}>Nghỉ việc</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showAdd && (
        <div style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.2)',zIndex:1000,display:'flex',alignItems:'center',justifyContent:'center'}}>
          <div style={{background:'#fff',padding:32,borderRadius:8,minWidth:340,boxShadow:'0 2px 16px rgba(0,0,0,0.12)'}}>
            <h2 style={{marginTop:0}}>Thêm nhân viên mới</h2>
            <div style={{marginBottom:12}}>
              <input value={newEmp.name} onChange={e=>setNewEmp({...newEmp,name:e.target.value})} placeholder="Họ tên" style={{width:'100%',padding:8,marginBottom:8,border:'1px solid #ccc',borderRadius:4}}/>
              <input value={newEmp.username} onChange={e=>setNewEmp({...newEmp,username:e.target.value})} placeholder="Username" style={{width:'100%',padding:8,marginBottom:8,border:'1px solid #ccc',borderRadius:4}}/>
              <input value={newEmp.age} onChange={e=>setNewEmp({...newEmp,age:e.target.value})} placeholder="Tuổi" type="number" style={{width:'100%',padding:8,marginBottom:8,border:'1px solid #ccc',borderRadius:4}}/>
              <input value={newEmp.address} onChange={e=>setNewEmp({...newEmp,address:e.target.value})} placeholder="Địa chỉ" style={{width:'100%',padding:8,marginBottom:8,border:'1px solid #ccc',borderRadius:4}}/>
              <input value={newEmp.phone} onChange={e=>setNewEmp({...newEmp,phone:e.target.value})} placeholder="Số điện thoại" style={{width:'100%',padding:8,marginBottom:8,border:'1px solid #ccc',borderRadius:4}}/>
              <select value={newEmp.shift} onChange={e=>setNewEmp({...newEmp,shift:e.target.value as 'day'|'night'})} style={{width:'100%',padding:8,marginBottom:8,border:'1px solid #ccc',borderRadius:4}}>
                <option value="day">Ca ngày</option>
                <option value="night">Ca đêm</option>
              </select>
              <input value="123456" disabled style={{width:'100%',padding:8,marginBottom:8,border:'1px solid #ccc',borderRadius:4,background:'#f5f5f5'}} placeholder="Mật khẩu mặc định"/>
            </div>
            <div style={{display:'flex',justifyContent:'flex-end',gap:8}}>
              <button onClick={()=>setShowAdd(false)} style={{padding:'8px 16px',borderRadius:4,border:'none',background:'#bdc3c7',color:'#fff',fontWeight:600,cursor:'pointer'}}>Hủy</button>
              <button
                onClick={async()=>{
                  if (!newEmp.username.trim()) {
                    alert('Username là bắt buộc!');
                    return;
                  }
                  try {
                    const res = await addUserAndAccount({
                      username: newEmp.username.trim(),
                      full_name: newEmp.name?.trim() || undefined,
                      age: newEmp.age?.trim() ? Number(newEmp.age) : undefined,
                      address: newEmp.address?.trim() || undefined,
                      phone: newEmp.phone?.trim() || undefined,
                      shift: newEmp.shift || 'day',
                    });
                    if (res?.success === false) {
                      alert(res?.message || 'Có lỗi xảy ra khi thêm nhân viên!');
                      return;
                    }
                    alert('Thêm nhân viên thành công!');
                    setShowAdd(false);
                    const data = await fetchEmployees();
                    setEmployees(data);
                  } catch (e: any) {
                    alert(e?.message || 'Có lỗi xảy ra khi thêm nhân viên!');
                  }
                }}
                style={{padding:'8px 16px',borderRadius:4,border:'none',background:'#27ae60',color:'#fff',fontWeight:600,cursor:'pointer'}}
              >Thêm</button>
            </div>
          </div>
        </div>
      )}
      <AdminPinModal
        open={modalAction !== null && modalAction.type !== 'add'}
        title="Xác nhận thao tác"
        onConfirm={performAction}
        onCancel={() => setModalAction(null)}
      />
    </AdminLayout>
  );
}
const th:React.CSSProperties={padding:10,fontSize:12,textTransform:'uppercase',color:'#7f8c8d',textAlign:'left'};
const td:React.CSSProperties={padding:10,fontSize:14};
const badge=(bg:string):React.CSSProperties=>({background:bg,color:'#fff',padding:'4px 8px',borderRadius:4,fontSize:12});