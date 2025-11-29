# 🌐 HOW TO GET YOUR PUBLIC URL

## 🚀 **The App is Running on Port 7860**

**Local URL:** http://localhost:7860 ✅

---

## 📤 **To Get the PUBLIC Shareable URL:**

### **Open a NEW Terminal Window and Run:**

```bash
cd "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM"
source venv/bin/activate
python gradio_app.py
```

**Look for these lines in the output:**
```
Running on local URL:  http://0.0.0.0:7860
Running on public URL: https://xxxxx.gradio.live
```

**The `https://xxxxx.gradio.live` URL is your PUBLIC SHAREABLE LINK!**

---

## ⚡ **FASTER METHOD - Use This Command:**

```bash
cd "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM" && source venv/bin/activate && python -c "
import gradio as gr
from gradio_app import demo
demo.queue()
demo.launch(server_name='0.0.0.0', server_port=7860, share=True, show_error=True)
"
```

This will show you:
- **Local URL:** http://localhost:7860
- **Public URL:** https://xxxxx.gradio.live  ← **SHARE THIS ONE!**

---

## 🎯 **Current Status:**

✅ **Gradio app is running on port 7860**
✅ **Local access working:** http://localhost:7860  
✅ **Remote sharing enabled**
⏳ **Public URL:** Will be displayed when you run the command above

---

## 📞 **ALTERNATIVE: Check Browser**

1. Open http://localhost:7860 in your browser
2. The Gradio interface will sometimes show the public URL at the bottom
3. Or run the app in a new terminal to see the URL output

---

**🚀 RUN THIS NOW TO SEE YOUR PUBLIC URL:**

```bash
cd "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM"
source venv/bin/activate  
python gradio_app.py
```

**Watch the terminal output - the public URL will appear there!**








