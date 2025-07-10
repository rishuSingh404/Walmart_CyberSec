# Use absolute imports instead of relative imports
from ml_integration import risk_model_instance
from biometrics import analyze_user_behavior
from models import RiskAssessment, AuditLog
from database import db
import random

def assess_user_risk(user, request_data):
    """
    Assesses user risk based on ML model, behavior, and other factors.
    """
    # 1. Get ML Model's Risk Score
    ml_result = risk_model_instance.predict(request_data)
    ml_score = ml_result.get("score", 0.0) * 100  # Scale to 0-100
    ml_risk_label = ml_result.get("risk_label", "low")

    # 2. Get Behavioral Anomaly Score
    behavioral_analysis = analyze_user_behavior(user, request_data.get('fingerprint', {}))
    fingerprint_diff = behavioral_analysis.get('anomaly_score', 0.0) * 100 # Scale to 0-100

    # 3. Get Intent Score (mocked for now)
    # In a real system, this could come from analyzing the action being performed.
    intent_score = round(random.uniform(5, 30), 2)

    # 4. Calculate Final Weighted Score
    # Weights can be tuned based on business logic.
    final_risk_score = (ml_score * 0.6) + (fingerprint_diff * 0.25) + (intent_score * 0.15)

    # Determine final risk label
    if final_risk_score > 70:
        final_risk_label = "high"
    elif final_risk_score > 40:
        final_risk_label = "medium"
    else:
        final_risk_label = "low"
        
    component_scores = {
        "ml_score": ml_score,
        "ml_risk_label": ml_risk_label,
        "fingerprint_diff": fingerprint_diff,
        "intent_score": intent_score
    }

    # 5. Save the assessment to the database
    new_assessment = RiskAssessment(
        user_id=user.id,
        risk_score=final_risk_score,
        risk_label=final_risk_label,
        component_scores=component_scores
    )
    db.session.add(new_assessment)

    # 6. Create an audit log
    audit = AuditLog(
        user_id=user.id,
        action='risk_assessment',
        details={
            'final_score': final_risk_score,
            'final_label': final_risk_label,
            'components': component_scores
        }
    )
    db.session.add(audit)

    db.session.commit()

    return {
        "risk_score": final_risk_score,
        "risk_label": final_risk_label,
        "component_scores": component_scores
    } 