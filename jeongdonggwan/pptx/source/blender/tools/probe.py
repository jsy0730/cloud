import bpy
cp = bpy.context.preferences.addons['cycles'].preferences
cp.refresh_devices() if hasattr(cp,'refresh_devices') else None
for t in ('HIP','OPTIX','CUDA','ONEAPI','METAL'):
    try:
        cp.compute_device_type = t
        cp.get_devices()
        print(t,[ (d.name,d.type,d.use) for d in cp.devices])
    except Exception as e:
        print(t,'ERR',str(e)[:60])
