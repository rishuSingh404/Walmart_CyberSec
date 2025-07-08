// Enhanced User Analytics Hook for Flask API Integration
import { useState, useEffect, useRef, useCallback } from 'react';
import { getBehaviorCollector } from '@/utils/behaviorCollector';
import { biometricsService, riskService, analyticsService } from '@/utils/flaskApi';
import { useToast } from '@/hooks/use-toast';

export interface FlaskAnalyticsData {
  fingerprint_analysis?: {
    is_anomaly: boolean;
    anomaly_score: number;
    confidence: number;
    anomalous_fields: string[];
  };
  risk_assessment?: {
    risk_score: number;
    risk_label: string;
    component_scores: {
      ml_score: number;
      fingerprint_diff: number;
      intent_score: number;
    };
  };
  session_analytics?: {
    session_id: string;
    start_time: string;
    duration: number;
    risk_level: string;
    events: any[];
  };
}

export interface UseFlaskAnalyticsProps {
  enabled?: boolean;
  updateInterval?: number;
  riskThreshold?: number;
  onRiskDetected?: (riskData: any) => void;
  onAnomalyDetected?: (anomalyData: any) => void;
}

export const useFlaskAnalytics = ({
  enabled = true,
  updateInterval = 30000, // 30 seconds
  riskThreshold = 50,
  onRiskDetected,
  onAnomalyDetected
}: UseFlaskAnalyticsProps = {}) => {
  const [analyticsData, setAnalyticsData] = useState<FlaskAnalyticsData>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isMonitoring, setIsMonitoring] = useState(false);
  
  const { toast } = useToast();
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const collectorRef = useRef(getBehaviorCollector());

  // Update fingerprint with Flask API
  const updateFingerprint = useCallback(async () => {
    if (!enabled) return;

    try {
      const metrics = collectorRef.current.getMetrics();
      const result = await biometricsService.updateFingerprint(metrics);
      
      console.log('Fingerprint updated:', result);
      return result;
    } catch (error: any) {
      console.error('Failed to update fingerprint:', error);
      setError('Failed to update fingerprint');
    }
  }, [enabled]);

  // Analyze current behavior for anomalies
  const analyzeFingerprint = useCallback(async () => {
    if (!enabled) return;

    try {
      const metrics = collectorRef.current.getMetrics();
      const analysis = await biometricsService.analyzeFingerprint(metrics);
      
      setAnalyticsData(prev => ({
        ...prev,
        fingerprint_analysis: analysis
      }));

      // Trigger anomaly callback if detected
      if (analysis.is_anomaly && onAnomalyDetected) {
        onAnomalyDetected(analysis);
        
        toast({
          title: "Anomaly Detected",
          description: `Unusual behavior detected with ${(analysis.confidence * 100).toFixed(1)}% confidence`,
          variant: "destructive",
        });
      }

      return analysis;
    } catch (error: any) {
      console.error('Failed to analyze fingerprint:', error);
      setError('Failed to analyze behavior');
    }
  }, [enabled, onAnomalyDetected, toast]);

  // Assess risk with current metrics
  const assessRisk = useCallback(async () => {
    if (!enabled) return;

    try {
      const metrics = collectorRef.current.getRiskAssessmentMetrics();
      const assessment = await riskService.assessRisk(metrics);
      
      setAnalyticsData(prev => ({
        ...prev,
        risk_assessment: assessment
      }));

      // Trigger risk callback if threshold exceeded
      if (assessment.risk_score > riskThreshold && onRiskDetected) {
        onRiskDetected(assessment);
        
        toast({
          title: "High Risk Detected",
          description: `Risk score: ${assessment.risk_score.toFixed(1)} (${assessment.risk_label})`,
          variant: "destructive",
        });
      }

      return assessment;
    } catch (error: any) {
      console.error('Failed to assess risk:', error);
      setError('Failed to assess risk');
    }
  }, [enabled, riskThreshold, onRiskDetected, toast]);

  // Get session analytics
  const getSessionAnalytics = useCallback(async () => {
    if (!enabled) return;

    try {
      const session = await analyticsService.getSessionAnalytics();
      
      setAnalyticsData(prev => ({
        ...prev,
        session_analytics: session
      }));

      return session;
    } catch (error: any) {
      console.error('Failed to get session analytics:', error);
      setError('Failed to get session analytics');
    }
  }, [enabled]);

  // Comprehensive analysis function
  const runFullAnalysis = useCallback(async () => {
    if (!enabled || isLoading) return;

    setIsLoading(true);
    setError(null);

    try {
      const [fingerprintAnalysis, riskAssessment, sessionData] = await Promise.allSettled([
        analyzeFingerprint(),
        assessRisk(),
        getSessionAnalytics()
      ]);

      // Log results for debugging
      console.log('Full analysis completed:', {
        fingerprint: fingerprintAnalysis,
        risk: riskAssessment,
        session: sessionData
      });

    } catch (error: any) {
      console.error('Full analysis failed:', error);
      setError('Analysis failed');
    } finally {
      setIsLoading(false);
    }
  }, [enabled, isLoading, analyzeFingerprint, assessRisk, getSessionAnalytics]);

  // Start continuous monitoring
  const startMonitoring = useCallback(() => {
    if (!enabled || isMonitoring) return;

    setIsMonitoring(true);
    
    // Run initial analysis
    runFullAnalysis();

    // Set up interval for continuous monitoring
    intervalRef.current = setInterval(() => {
      runFullAnalysis();
    }, updateInterval);

    console.log(`Started Flask analytics monitoring with ${updateInterval}ms interval`);
  }, [enabled, isMonitoring, runFullAnalysis, updateInterval]);

  // Stop monitoring
  const stopMonitoring = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setIsMonitoring(false);
    console.log('Stopped Flask analytics monitoring');
  }, []);

  // Get current behavior metrics
  const getCurrentMetrics = useCallback(() => {
    return collectorRef.current.getMetrics();
  }, []);

  // Get risk assessment metrics
  const getRiskMetrics = useCallback(() => {
    return collectorRef.current.getRiskAssessmentMetrics();
  }, []);

  // Auto-start monitoring when component mounts
  useEffect(() => {
    if (enabled) {
      startMonitoring();
    }

    // Cleanup on unmount
    return () => {
      stopMonitoring();
    };
  }, [enabled, startMonitoring, stopMonitoring]);

  return {
    // Data
    analyticsData,
    isLoading,
    error,
    isMonitoring,
    
    // Actions
    updateFingerprint,
    analyzeFingerprint,
    assessRisk,
    getSessionAnalytics,
    runFullAnalysis,
    startMonitoring,
    stopMonitoring,
    getCurrentMetrics,
    getRiskMetrics,
    
    // Utilities
    clearError: () => setError(null),
    resetData: () => setAnalyticsData({}),
  };
};
