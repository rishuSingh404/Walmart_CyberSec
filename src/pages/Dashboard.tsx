
import { Layout } from '@/components/layout/Layout';
import { useAuth } from '@/hooks/useAuth';
import { useFlaskAnalytics } from '@/hooks/useFlaskAnalytics';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useNavigate } from 'react-router-dom';
import { BarChart3, Settings, User, TrendingUp, Shield, AlertTriangle, Activity } from 'lucide-react';
import { useEffect, useState } from 'react';
import { analyticsService } from '@/utils/flaskApi';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [dashboardStats, setDashboardStats] = useState({
    active_sessions: 0,
    high_risk_count: 0,
    login_attempts: 0,
    blocked_attempts: 0
  });

  const {
    analyticsData,
    isLoading,
    error,
    getCurrentMetrics,
    runFullAnalysis
  } = useFlaskAnalytics({
    enabled: true,
    updateInterval: 30000,
    riskThreshold: 70,
    onRiskDetected: (riskData) => {
      console.log('High risk detected:', riskData);
    },
    onAnomalyDetected: (anomalyData) => {
      console.log('Anomaly detected:', anomalyData);
    }
  });

  // Fetch dashboard statistics
  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        const stats = await analyticsService.getDashboardAnalytics();
        setDashboardStats(stats);
      } catch (error) {
        console.error('Failed to fetch dashboard stats:', error);
      }
    };

    fetchDashboardStats();
    // Refresh stats every minute
    const interval = setInterval(fetchDashboardStats, 60000);
    return () => clearInterval(interval);
  }, []);

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  const currentMetrics = getCurrentMetrics();
  const riskData = analyticsData.risk_assessment;
  const fingerprintData = analyticsData.fingerprint_analysis;

  const getRiskColor = (score?: number) => {
    if (!score) return 'bg-gray-500';
    if (score < 30) return 'bg-green-500';
    if (score < 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getRiskLabel = (score?: number) => {
    if (!score) return 'Unknown';
    if (score < 30) return 'Low';
    if (score < 70) return 'Medium';
    return 'High';
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back, {user?.name || user?.email}!</p>
        </div>
        
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card className="cursor-pointer hover:shadow-lg transition-shadow" onClick={() => handleNavigate('/profile')}>
            <CardHeader>
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-blue-600" />
                <CardTitle>Profile</CardTitle>
              </div>
              <CardDescription>Manage your account settings</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Update your personal information and preferences.
              </p>
              <Button variant="outline" className="w-full">
                View Profile
              </Button>
            </CardContent>
          </Card>
          
          <Card className="cursor-pointer hover:shadow-lg transition-shadow" onClick={() => handleNavigate('/admin')}>
            <CardHeader>
              <div className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-green-600" />
                <CardTitle>Analytics</CardTitle>
              </div>
              <CardDescription>View your activity stats</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Track your progress and performance metrics.
              </p>
              <Button variant="outline" className="w-full">
                View Analytics
              </Button>
            </CardContent>
          </Card>
          
          <Card className="cursor-pointer hover:shadow-lg transition-shadow" onClick={() => handleNavigate('/settings')}>
            <CardHeader>
              <div className="flex items-center space-x-2">
                <Settings className="h-5 w-5 text-purple-600" />
                <CardTitle>Settings</CardTitle>
              </div>
              <CardDescription>Configure your preferences</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Customize your experience and notifications.
              </p>
              <Button variant="outline" className="w-full">
                Open Settings
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Security Status Section */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardDescription className="flex items-center">
                  <Shield className="h-4 w-4 mr-2" />
                  Risk Score
                </CardDescription>
                <Badge variant={riskData?.risk_score && riskData.risk_score > 50 ? "destructive" : "default"}>
                  {getRiskLabel(riskData?.risk_score)}
                </Badge>
              </div>
              <CardTitle className="text-2xl">
                {riskData?.risk_score?.toFixed(1) || '--'}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`w-full h-2 rounded-full ${getRiskColor(riskData?.risk_score)}`} />
              <p className="text-xs text-muted-foreground mt-2">
                Real-time behavioral risk assessment
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardDescription className="flex items-center">
                  <Activity className="h-4 w-4 mr-2" />
                  Behavior Status
                </CardDescription>
                <Badge variant={fingerprintData?.is_anomaly ? "destructive" : "default"}>
                  {fingerprintData?.is_anomaly ? "Anomaly" : "Normal"}
                </Badge>
              </div>
              <CardTitle className="text-2xl">
                {fingerprintData?.confidence ? `${(fingerprintData.confidence * 100).toFixed(0)}%` : '--'}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                Confidence level: {fingerprintData?.anomaly_score ? `${(fingerprintData.anomaly_score * 100).toFixed(1)}% anomaly` : 'No data'}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center">
                <AlertTriangle className="h-4 w-4 mr-2" />
                <CardDescription>Session Duration</CardDescription>
              </div>
              <CardTitle className="text-2xl">
                {currentMetrics.session_duration ? `${Math.floor(currentMetrics.session_duration / 60000)}m` : '--'}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                Actions: {currentMetrics.click_count} clicks, {currentMetrics.typing_speed?.toFixed(0) || 0}ms avg typing
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Stats Section */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Active Sessions</CardDescription>
              <CardTitle className="text-2xl">{dashboardStats.active_sessions}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                <Activity className="inline h-3 w-3 mr-1" />
                Currently active
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>High Risk Sessions</CardDescription>
              <CardTitle className="text-2xl">{dashboardStats.high_risk_count}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                <AlertTriangle className="inline h-3 w-3 mr-1" />
                Requires attention
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Login Attempts</CardDescription>
              <CardTitle className="text-2xl">{dashboardStats.login_attempts}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                Total today
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Blocked Attempts</CardDescription>
              <CardTitle className="text-2xl">{dashboardStats.blocked_attempts}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                <Shield className="inline h-3 w-3 mr-1" />
                Security blocks
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Manual Analysis Section */}
        <Card>
          <CardHeader>
            <CardTitle>Security Analysis</CardTitle>
            <CardDescription>
              Manual behavioral analysis and risk assessment
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span>Current Behavioral Metrics:</span>
              <Button
                variant="outline"
                onClick={runFullAnalysis}
                disabled={isLoading}
              >
                {isLoading ? 'Analyzing...' : 'Run Analysis'}
              </Button>
            </div>
            
            {error && (
              <div className="text-sm text-red-600 bg-red-50 p-2 rounded">
                Error: {error}
              </div>
            )}
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Typing Speed:</span>
                <div className="font-mono">{currentMetrics.typing_speed?.toFixed(0) || 0}ms</div>
              </div>
              <div>
                <span className="text-muted-foreground">Mouse Distance:</span>
                <div className="font-mono">{currentMetrics.mouse_distance?.toFixed(0) || 0}px</div>
              </div>
              <div>
                <span className="text-muted-foreground">Scroll Depth:</span>
                <div className="font-mono">{(currentMetrics.scroll_depth * 100)?.toFixed(1) || 0}%</div>
              </div>
              <div>
                <span className="text-muted-foreground">Click Count:</span>
                <div className="font-mono">{currentMetrics.click_count}</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
};

export default Dashboard;
