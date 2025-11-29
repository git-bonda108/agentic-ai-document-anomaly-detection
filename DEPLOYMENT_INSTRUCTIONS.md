
# 🚀 Hugging Face Spaces Deployment Instructions

## Step 1: Create HF Space
1. Go to https://huggingface.co/new-space
2. Choose name: `doc-anomaly-detection`
3. Select SDK: **Gradio**
4. Set visibility: **Public** (for sharing)

## Step 2: Upload Files
Upload these files to your HF Space:

### Core Application Files
- `gradio_app.py` - Main Gradio application
- `orchestrator.py` - Processing orchestrator
- `requirements.txt` - Dependencies

### Agent Directory
- `agents/` - Complete directory with all agent files

### Sample Data
- `sample_data/` - Sample documents for testing

### Configuration
- `README.md` - Space description and documentation

## Step 3: Deploy
1. HF Spaces will automatically build and deploy
2. Wait for "Building" to complete (5-10 minutes)
3. Your app will be live at: `https://huggingface.co/spaces/[username]/doc-anomaly-detection`

## Step 4: Share
- Copy the public URL
- Share with HP stakeholders
- Use for demos and presentations

## Troubleshooting

### Build Failures
- Check `requirements.txt` for version conflicts
- Ensure all dependencies are compatible
- Review build logs for specific errors

### Runtime Errors
- Verify all files are uploaded correctly
- Check agent imports and dependencies
- Test with sample documents first

### Performance Issues
- HF Spaces has resource limits
- Optimize for concurrent users
- Consider upgrading to paid tier for production

## Customization

### Branding
- Update title and description in `README.md`
- Modify colors in `gradio_app.py` theme settings
- Add HP logo and branding elements

### Features
- Add authentication for enterprise use
- Implement custom business rules
- Add additional document types

## Support
- HF Spaces Documentation: https://huggingface.co/docs/hub/spaces
- Gradio Documentation: https://gradio.app/docs
- Issues: Create GitHub issue or HF Space discussion
