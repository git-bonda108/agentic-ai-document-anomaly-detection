# ML Upgrade Implementation Roadmap

## Quick Start Guide

### Step 1: Install Dependencies
```bash
pip install -r requirements_ml.txt
```

### Step 2: Set Up Environment Variables
Create `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
LANGSMITH_API_KEY=your_langsmith_api_key  # Optional but recommended
LANGSMITH_PROJECT=doc-anomaly-detection
```

### Step 3: Initialize Components
1. **Vector Database**: ChromaDB auto-initializes on first use
2. **MLflow**: Initialize with `mlflow ui` for model tracking
3. **Observability**: LangSmith auto-initializes with API key

---

## Implementation Phases (Detailed)

### Phase 1: ML Foundation ✅

**Goal**: Get basic ML model working with inference

**Tasks:**
1. ✅ Create feature engineering module
2. ✅ Build training data from rule-based system outputs
3. ✅ Train XGBoost baseline model
4. ✅ Implement model inference
5. ✅ Basic Streamlit page for predictions
6. ✅ Save/load models with MLflow

**Files to Create:**
- `ml_models/feature_engineer.py`
- `ml_models/anomaly_classifier.py`
- `ml_models/model_trainer.py`
- `training/data_preparation.py`

**Expected Output:**
- Working ML model that can predict anomalies
- Basic Streamlit interface showing predictions

---

### Phase 2: Observability & Agentic AI ✅

**Goal**: Track all agent operations with full observability

**Tasks:**
1. ✅ Integrate OpenAI SDK
2. ✅ Set up LangSmith tracking
3. ✅ Implement agent execution tracing
4. ✅ Create observability dashboard
5. ✅ Track token usage and costs
6. ✅ Log all agent decisions

**Files to Create:**
- `observability/langsmith_tracker.py`
- `observability/agent_monitor.py`
- `agents/ml_prediction_agent.py` (OpenAI-integrated)
- `streamlit_app/pages/5_👁️_Observability.py`

**Expected Output:**
- All agent calls visible in LangSmith
- Real-time observability dashboard
- Cost tracking per operation

---

### Phase 3: Human-in-the-Loop & RL ✅

**Goal**: Enable human feedback and reinforcement learning

**Tasks:**
1. ✅ Design feedback UI in Streamlit
2. ✅ Store feedback in database
3. ✅ Implement RL environment
4. ✅ Set up PPO training loop
5. ✅ Update model from feedback
6. ✅ Test complete feedback loop

**Files to Create:**
- `agents/human_feedback_agent.py`
- `training/reinforcement_learning.py`
- `streamlit_app/components/feedback_ui.py`
- `streamlit_app/pages/3_👤_Human_Feedback.py`

**Expected Output:**
- Users can provide feedback on predictions
- Model improves from feedback
- RL agent learns optimal detection policy

---

### Phase 4: Memory System ✅

**Goal**: Persistent memory for context-aware predictions

**Tasks:**
1. ✅ Set up ChromaDB
2. ✅ Implement document embeddings
3. ✅ Create memory retrieval system
4. ✅ Build episodic memory (similar cases)
5. ✅ Memory cleanup strategies

**Files to Create:**
- `memory/vector_store.py`
- `memory/episodic_memory.py`
- `memory/memory_manager.py`
- `agents/memory_agent.py`

**Expected Output:**
- System remembers past cases
- Retrieves similar documents automatically
- Context-aware predictions

---

### Phase 5: Advanced Metrics & Visualization ✅

**Goal**: Comprehensive ML metrics dashboard

**Tasks:**
1. ✅ Implement all metrics (F1, precision, recall, etc.)
2. ✅ Create confusion matrix
3. ✅ Build ROC/PR curves
4. ✅ Feature importance plots
5. ✅ Per-anomaly-type metrics
6. ✅ Learning curves

**Files to Create:**
- `metrics/evaluator.py`
- `metrics/visualizations.py`
- `metrics/confusion_matrix.py`
- `streamlit_app/pages/4_📊_Metrics_Dashboard.py`

**Expected Output:**
- Complete metrics dashboard
- All visualizations working
- Model performance tracking

---

### Phase 6: Integration & Polish ✅

**Goal**: Complete integrated system

**Tasks:**
1. ✅ Integrate all components
2. ✅ End-to-end testing
3. ✅ Performance optimization
4. ✅ UI/UX improvements
5. ✅ Documentation
6. ✅ Deployment preparation

**Files to Update:**
- All integration points
- Main Streamlit app
- Documentation files

**Expected Output:**
- Production-ready system
- Complete documentation
- Deployment scripts

---

## Testing Strategy

### Unit Tests
- Test each ML model component
- Test feature engineering
- Test memory retrieval
- Test observability tracking

### Integration Tests
- End-to-end document processing
- Feedback loop functionality
- Model training pipeline
- Memory integration

### Performance Tests
- Inference latency
- Training time
- Memory usage
- Token usage efficiency

---

## Success Criteria

### Technical Metrics
- ✅ F1 Score > 0.85
- ✅ Precision > 0.80
- ✅ Recall > 0.90
- ✅ Inference < 2 seconds
- ✅ All metrics visualizations working

### User Experience
- ✅ Streamlit app is intuitive
- ✅ Feedback process is smooth
- ✅ Observability dashboard is clear
- ✅ Metrics are understandable

### Business Metrics
- ✅ Reduced false positives
- ✅ Improved detection rate
- ✅ Cost-effective operation
- ✅ Scalable architecture

---

## Deployment Considerations

### Development
- Local Streamlit app
- SQLite database
- Local ChromaDB

### Production
- Streamlit Cloud / Docker
- PostgreSQL database
- ChromaDB persistence layer
- Redis for caching
- MLflow model serving

---

## Notes

- Start with Phase 1, validate ML model works
- Add observability early (Phase 2) for debugging
- Implement feedback loop before full RL (Phase 3)
- Memory system can be added incrementally (Phase 4)
- Metrics dashboard is crucial for monitoring (Phase 5)





