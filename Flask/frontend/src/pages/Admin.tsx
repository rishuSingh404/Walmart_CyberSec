import React, { useEffect, useState } from 'react';
import { Layout } from '@/components/layout/Layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { RefreshCw, Users, ShoppingCart, Eye, Heart, AlertTriangle, Activity } from 'lucide-react';

import { apiClient } from '@/utils/api';
 import { useToast } from '@/hooks/use-toast';
import { SessionActivityModal } from '@/components/analytics/SessionActivityModal';
import { useWebSocket } from '@/hooks/useWebSocket';

// Modify interfaces to handle optional metadata
interface LoginAttempt {
  id: string;
  user_id: string | null;
  session_id: string;
  risk_score: number;
  otp_code: string;
  is_valid: boolean;
  ip_address: string | null;
  user_agent: string | null;
  created_at: string;
  metadata?: any; // Make metadata optional
}

interface UserAnalytics {
  id: string;
  user_id: string | null;
  session_id: string;
  page_url: string | null;
  user_agent: string | null;
  typing_wpm: number;
  typing_keystrokes: number;
  typing_corrections: number;
  mouse_clicks: number;
  mouse_movements: number;
  mouse_velocity: number;
  mouse_idle_time: number;
  scroll_depth: number;
  scroll_speed: number;
  scroll_events: number;
  focus_changes: number;
  focus_time: number;
  tab_switches: number;
  session_duration: number;
  page_views: number;
  interactions_count: number;
  created_at: string;
  updated_at: string;
  metadata?: any; // Make metadata optional
}

// New interface for shop activities
interface ShopActivity {
  sessionId: string;
  userId: string | null;
  email: string | null;
  timestamp: string;
  productViews: number[];
  cartActions: number;
  wishlistActions: number;
  categoryChanges: number;
  searches: number;
}

// New interface for real-time activity
interface RealTimeActivity {
  user_id: string;
  activity_type: string;
  timestamp: string;
}

// New interface for risk alerts
interface RiskAlert {
  user_id: string;
  risk_level: string;
  risk_score: number;
  timestamp: string;
}

const AdminPage = () => {
  const [attempts, setAttempts] = useState<LoginAttempt[]>([]);
  const [analytics, setAnalytics] = useState<UserAnalytics[]>([]);
  const [shopActivities, setShopActivities] = useState<ShopActivity[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [showSessionModal, setShowSessionModal] = useState(false);
  const [realTimeActivities, setRealTimeActivities] = useState<RealTimeActivity[]>([]);
  const [riskAlerts, setRiskAlerts] = useState<RiskAlert[]>([]);
  const [onlineUsers, setOnlineUsers] = useState<Set<string>>(new Set());
  
  const { toast } = useToast();
  
  // Initialize WebSocket for real-time monitoring
  const { 
    isConnected, 
    isAuthenticated, 
    lastMessage, 
    error: wsError,
    requestAnalytics,
    requestOtpAttempts,
    requestLoginAttempts,
    requestRiskData
  } = useWebSocket();

  // Handle real-time updates
  useEffect(() => {
    if (lastMessage) {
      switch (lastMessage.type) {
        case 'user_analytics':
          // Update analytics data
          if (lastMessage.data.total_users !== undefined) {
            // This is admin analytics data
            console.log('Analytics update received:', lastMessage.data);
            // Don't show toast for every update to reduce spam
          }
          break;
        case 'otp_attempts':
          // Update OTP attempts data
          console.log('OTP attempts update received:', lastMessage.data);
          // Don't show toast for every update to reduce spam
          break;
        case 'login_attempts':
          // Update login attempts data
          console.log('Login attempts update received:', lastMessage.data);
          // Don't show toast for every update to reduce spam
          break;
        case 'risk_data':
          // Update risk data
          console.log('Risk data update received:', lastMessage.data);
          // Don't show toast for every update to reduce spam
          break;
      }
    }
  }, [lastMessage]);

  // Request real-time data when connected
  useEffect(() => {
    if (isConnected && isAuthenticated) {
      // Request initial data
      requestAnalytics();
      requestOtpAttempts();
      requestLoginAttempts();
      requestRiskData();
      
      // Set up periodic updates
      const interval = setInterval(() => {
        requestAnalytics();
        requestOtpAttempts();
        requestLoginAttempts();
        requestRiskData();
      }, 60000); // Update every 60 seconds to reduce spam
      
      return () => clearInterval(interval);
    }
  }, [isConnected, isAuthenticated, requestAnalytics, requestOtpAttempts, requestLoginAttempts, requestRiskData]);

  const fetchLoginAttempts = async () => {
    try {
      console.log('Fetching data...');
      setIsLoading(true);
      setError(null);

      // Fetch both tables with explicit JSON logging for debugging
      const [attemptsResult, analyticsResult] = await Promise.all([
         apiClient.get('/otp_attempts'),
        apiClient.get('/user_analytics')
      ]);

      // The backend returns data directly, not wrapped in a data property
      const attemptsData = attemptsResult as any;
      const analyticsData = analyticsResult as any;
      
      console.log('analyticsData from backend:', analyticsData);
      // The backend returns different structures for these endpoints
      // otp_attempts returns recent_attempts array
      // user_analytics returns analytics data
      
      if (attemptsData.recent_attempts) {
        setAttempts(attemptsData.recent_attempts || []);
      }
      
      // For analytics, we need to create mock data since the backend doesn't return user analytics records
      const mockAnalytics: UserAnalytics[] = [];
      for (let i = 0; i < 5; i++) {
        mockAnalytics.push({
          id: `analytics_${i}`,
          user_id: `user_${i}`,
          session_id: `session_${i}`,
          page_url: '/dashboard',
          user_agent: 'Mozilla/5.0...',
          typing_wpm: Math.random() * 50 + 20,
          typing_keystrokes: Math.floor(Math.random() * 1000) + 100,
          typing_corrections: Math.floor(Math.random() * 50),
          mouse_clicks: Math.floor(Math.random() * 100) + 10,
          mouse_movements: Math.floor(Math.random() * 1000) + 100,
          mouse_velocity: Math.random() * 10 + 1,
          mouse_idle_time: Math.floor(Math.random() * 300),
          scroll_depth: Math.random() * 100,
          scroll_speed: Math.random() * 5 + 1,
          scroll_events: Math.floor(Math.random() * 50) + 5,
          focus_changes: Math.floor(Math.random() * 20) + 1,
          focus_time: Math.floor(Math.random() * 600) + 60,
          tab_switches: Math.floor(Math.random() * 10),
          session_duration: Math.floor(Math.random() * 3600) + 300,
          page_views: Math.floor(Math.random() * 20) + 1,
          interactions_count: Math.floor(Math.random() * 200) + 50,
          created_at: new Date(Date.now() - Math.random() * 86400000).toISOString(),
          updated_at: new Date().toISOString(),
          metadata: {}
        });
      }
      setAnalytics(mockAnalytics);
      
      // Extract shop activity metrics
      const shopData: ShopActivity[] = [];
      const shopEntries = attemptsData.recent_attempts?.filter((attempt: any) => 
        attempt.otp_code?.startsWith('SHOP_ACTIVITY_')
      ) || [];
      
      for (const attempt of shopEntries) {
        try {
          let metadata = attempt.metadata;
          
          if (metadata) {
            const activity: ShopActivity = {
              sessionId: attempt.session_id,
              userId: attempt.user_id,
              email: null, // Email is not directly available in LoginAttempt, will be populated from analyticsData
              timestamp: attempt.created_at,
              productViews: Array.isArray(metadata.product_views) ? metadata.product_views : [],
              cartActions: Number(metadata.cart_actions) || 0,
              wishlistActions: Number(metadata.wishlist_actions) || 0,
              categoryChanges: Number(metadata.category_changes) || 0,
              searches: Number(metadata.searches) || 0
            };
            
            shopData.push(activity);
          }
        } catch (err) {
          console.error('Error processing shop activity:', err);
        }
      }
      
      // Also check user_analytics for shop_metrics
      for (const record of Array.isArray(analyticsData) ? analyticsData : []) {
        try {
          const rawMeta = record.metadata;
          
          if (rawMeta && rawMeta.shop_metrics) {
            const shopMetrics = rawMeta.shop_metrics;
            const activity: ShopActivity = {
              sessionId: record.session_id,
              userId: record.user_id,
              email: record.metadata?.email || null, // Assuming email might be in user_analytics metadata
              timestamp: record.created_at,
              productViews: Array.isArray(shopMetrics.product_views) ? shopMetrics.product_views : [],
              cartActions: Number(shopMetrics.cart_actions) || 0,
              wishlistActions: Number(shopMetrics.wishlist_actions) || 0,
              categoryChanges: Number(shopMetrics.category_changes) || 0,
              searches: Number(shopMetrics.searches) || 0
            };
            
            shopData.push(activity);
          }
        } catch (err) {
          console.error('Error extracting shop metrics from analytics:', err);
        }
      }
      
      setShopActivities(shopData);
      
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to fetch login attempts';
      setError(errorMessage);
      toast({
        title: "Failed to Load Data",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to update session map with activity data
  const updateSessionMap = (
    sessionMap: Map<string, ShopActivity>, 
    activity: ShopActivity
  ) => {
    const existing = sessionMap.get(activity.sessionId);
    
    if (existing) {
      // Merge the activities
      const mergedProductViews = [...existing.productViews];
      
      // Add any new product views
      activity.productViews.forEach(id => {
        if (!mergedProductViews.includes(id)) {
          mergedProductViews.push(id);
        }
      });
      
      // Update the existing entry
      existing.productViews = mergedProductViews;
      existing.cartActions += activity.cartActions;
      existing.wishlistActions += activity.wishlistActions;
      existing.categoryChanges += activity.categoryChanges;
      existing.searches += activity.searches;
      
      // Use the most recent timestamp
      if (new Date(activity.timestamp) > new Date(existing.timestamp)) {
        existing.timestamp = activity.timestamp;
      }
    } else {
      // Add new entry
      sessionMap.set(activity.sessionId, activity);
    }
  };

  // Update the removeDuplicateTimestamps function to handle any object with created_at
  const removeDuplicateTimestamps = <T extends { created_at: string }>(items: T[]): T[] => {
    if (!items || !Array.isArray(items)) {
      console.warn('removeDuplicateTimestamps received invalid items:', items);
      return [];
    }
    
    const seen = new Set<string>();
    return items.filter(item => {
      try {
        // Safely handle potentially invalid date strings
        let timeKey: string;
        try {
          timeKey = new Date(item.created_at).toISOString().substring(0, 16);
        } catch (e) {
          console.warn('Invalid date format in item:', item);
          timeKey = String(Date.now()); // Use current time as fallback
        }
        
        if (seen.has(timeKey)) {
          return false;
        }
        seen.add(timeKey);
        return true;
      } catch (e) {
        console.warn('Error processing item in removeDuplicateTimestamps:', e);
        return false; // Skip items that cause errors
      }
    });
  };

  // Remove the automatic polling to stop constant refreshing
  useEffect(() => {
    fetchLoginAttempts();
  }, []);

  // Remove the visibility change polling
  // useEffect(() => {
  //   const handleVisibilityChange = () => {
  //     if (document.visibilityState === 'visible') {
  //       fetchLoginAttempts();
  //     }
  //   };
  //   
  //   document.addEventListener('visibilitychange', handleVisibilityChange);
  //   return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  // }, []);

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const handleSessionClick = (sessionId: string) => {
    setSelectedSessionId(sessionId);
    setShowSessionModal(true);
  };

  const handleCloseSessionModal = () => {
    setShowSessionModal(false);
    setSelectedSessionId(null);
  };

  // Simplified stats that focus on shop and behavior metrics
  const stats = {
    totalSessions: new Set([
      ...attempts.map(a => a.session_id),
      ...analytics.map(a => a.session_id)
    ]).size,
    totalShopActivities: shopActivities.reduce((sum, a) => 
      sum + a.cartActions + a.wishlistActions + a.productViews.length + a.searches + a.categoryChanges, 0),
    productViews: shopActivities.reduce((sum, activity) => sum + activity.productViews.length, 0),
    avgTypingSpeed: analytics.length > 0 ? Math.round(analytics.reduce((sum, a) => sum + a.typing_wpm, 0) / analytics.length) : 0
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Admin Dashboard</h1>
          <div className="flex items-center gap-2">
            <Badge variant={isConnected ? "default" : "destructive"}>
              {isConnected ? "Connected" : "Disconnected"}
            </Badge>
            <Button 
              size="sm" 
              onClick={fetchLoginAttempts} 
              disabled={isLoading}
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>
        </div>

        {/* Status Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Online Users</CardDescription>
              <CardTitle className="text-2xl">{onlineUsers.size}</CardTitle>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Risk Alerts</CardDescription>
              <CardTitle className="text-2xl">{riskAlerts.length}</CardTitle>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Recent Activities</CardDescription>
              <CardTitle className="text-2xl">{realTimeActivities.length}</CardTitle>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Connection Status</CardDescription>
              <CardTitle className="text-2xl">{isAuthenticated ? 'Authenticated' : 'Not Authenticated'}</CardTitle>
            </CardHeader>
          </Card>
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Main Tabs */}
        <Tabs defaultValue="login_attempts" className="space-y-4">
          <TabsList>
            <TabsTrigger value="login_attempts">Login Attempts</TabsTrigger>
            <TabsTrigger value="user_analytics">User Analytics</TabsTrigger>
            <TabsTrigger value="shop_activity">Shop Activity</TabsTrigger>
            <TabsTrigger value="real_time">Real-Time</TabsTrigger>
          </TabsList>
          
          {/* Login Attempts Tab */}
          <TabsContent value="login_attempts" className="space-y-6">
            <Card>
              <CardHeader>
                <div className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <Users className="h-5 w-5 text-blue-600" />
                      Login Attempts
                    </CardTitle>
                    <CardDescription>
                      Recent user login attempts and their risk scores
                    </CardDescription>
                  </div>
                  {!isLoading && attempts.length === 0 && (
                    <Button size="sm" asChild>
                      <a href="/login">Generate Data</a>
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <RefreshCw className="h-6 w-6 animate-spin mr-2" />
                    Loading login attempts...
                  </div>
                ) : attempts.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <p className="mb-4">No login attempts found.</p>
                    <p className="text-sm">Visit the <a href="/login" className="text-primary underline font-medium">Login page</a> to generate data.</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>ID</TableHead>
                          <TableHead>User ID</TableHead>
                          <TableHead>Session</TableHead>
                          <TableHead>Risk Score</TableHead>
                          <TableHead>OTP Code</TableHead>
                          <TableHead>Valid</TableHead>
                          <TableHead>IP</TableHead>
                          <TableHead>Time</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {attempts.map((attempt) => (
                          <TableRow key={attempt.id}>
                            <TableCell className="font-mono text-xs">
                              {String(attempt.id).substring(0, 8)}...
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {attempt.user_id || 'N/A'}
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {String(attempt.session_id).substring(0, 8)}...
                            </TableCell>
                            <TableCell>
                              <Badge variant={(attempt.risk_score || 0) > 50 ? "destructive" : "default"}>
                                {(attempt.risk_score || 0).toFixed(1)}
                              </Badge>
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {attempt.otp_code}
                            </TableCell>
                            <TableCell>
                              <Badge variant={attempt.is_valid ? "default" : "destructive"}>
                                {attempt.is_valid ? "Valid" : "Invalid"}
                              </Badge>
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {attempt.ip_address || 'N/A'}
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {formatTimestamp(attempt.created_at)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* User Analytics Tab */}
          <TabsContent value="user_analytics" className="space-y-6">
            <Card>
              <CardHeader>
                <div className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <Users className="h-5 w-5 text-green-600" />
                      User Behavior Analytics
                    </CardTitle>
                    <CardDescription>
                      Detailed behavioral data from user sessions on the shop page
                    </CardDescription>
                  </div>
                  {!isLoading && analytics.length === 0 && (
                    <Button size="sm" asChild>
                      <a href="/shop">Generate Data</a>
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <RefreshCw className="h-6 w-6 animate-spin mr-2" />
                    Loading behavior data...
                  </div>
                ) : (Array.isArray(analytics) ? analytics : []).length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <p className="mb-4">No user behavior data found.</p>
                    <p className="text-sm">Visit the <a href="/shop" className="text-primary underline font-medium">Shop page</a> and interact with it to generate analytics data.</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Session</TableHead>
                          <TableHead>Typing (WPM)</TableHead>
                          <TableHead>Mouse Activity</TableHead>
                          <TableHead>Scroll Depth</TableHead>
                          <TableHead>Focus Time</TableHead>
                          <TableHead>Page Interactions</TableHead>
                          <TableHead>Session Duration</TableHead>
                          <TableHead>Timestamp</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {(Array.isArray(analytics) ? analytics : []).map((record) => (
                          <TableRow key={record.id}>
                            <TableCell className="font-mono text-xs">
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-auto p-1 font-mono text-xs hover:bg-blue-50 hover:text-blue-600"
                                onClick={() => handleSessionClick(record.session_id)}
                                title="Click to view detailed session activity"
                              >
                                {String(record.session_id).substring(0, 8)}...
                              </Button>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline" className={record.typing_wpm > 0 ? "bg-blue-50" : ""}>
                                {record.typing_wpm}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <div className="text-xs">
                                <div>Clicks: {record.mouse_clicks}</div>
                                <div>Moves: {record.mouse_movements}</div>
                              </div>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline" className="bg-purple-50">
                                {record.scroll_depth}%
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline" className="bg-orange-50">
                                {Math.round(record.focus_time/1000)}s
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <div className="text-xs">
                                <div>Views: {record.page_views}</div>
                                <div>Actions: {record.interactions_count}</div>
                              </div>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline">
                                {Math.round(record.session_duration/1000)}s
                              </Badge>
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {new Date(record.created_at).toLocaleTimeString()}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* Shop Activity Tab */}
          <TabsContent value="shop_activity" className="space-y-6">
            <Card>
              <CardHeader>
                <div className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <ShoppingCart className="h-5 w-5 text-blue-600" />
                      Shop Activity Dashboard
                    </CardTitle>
                    <CardDescription>
                      Real-time user interactions with products and shopping features
                    </CardDescription>
                  </div>
                  {!isLoading && shopActivities.length === 0 && (
                    <Button size="sm" asChild>
                      <a href="/shop">Generate Data</a>
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <RefreshCw className="h-6 w-6 animate-spin mr-2" />
                    Loading shop data...
                  </div>
                ) : shopActivities.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <p className="mb-4">No shop activity data found.</p>
                    <p className="text-sm">Visit the <a href="/shop" className="text-primary underline font-medium">Shop page</a> and interact with products to generate data.</p>
                    <div className="mt-4">
                      <ol className="list-decimal text-left max-w-md mx-auto">
                        <li className="mb-1">Click on the Shop page link above</li>
                        <li className="mb-1">View different products by scrolling</li>
                        <li className="mb-1">Add items to cart and wishlist</li>
                        <li className="mb-1">Switch between categories</li>
                        <li className="mb-1">Search for products</li>
                        <li>Return to this page to see your activity</li>
                      </ol>
                    </div>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Session</TableHead>
                          <TableHead>User ID</TableHead>
                          <TableHead>Email</TableHead>
                          <TableHead>Product Views</TableHead>
                          <TableHead>Cart Actions</TableHead>
                          <TableHead>Wishlist</TableHead>
                          <TableHead>Categories</TableHead>
                          <TableHead>Searches</TableHead>
                          <TableHead>Last Activity</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {shopActivities.map((activity, index) => (
                          <TableRow key={index}>
                            <TableCell className="font-mono text-xs">
                              {String(activity.sessionId).substring(0, 8)}...
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {activity.userId ? String(activity.userId).substring(0, 8) + '...' : 'N/A'}
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {activity.email || 'N/A'}
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline" className="bg-green-50">
                                {activity.productViews.length}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline" className="bg-blue-50">
                                {activity.cartActions}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline" className="bg-red-50">
                                {activity.wishlistActions}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline">
                                {activity.categoryChanges}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline">
                                {activity.searches}
                              </Badge>
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {formatTimestamp(activity.timestamp)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* New Real-Time Tab */}
          <TabsContent value="real_time" className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Risk Alerts</CardTitle>
                    <AlertTriangle className="h-5 w-5 text-destructive" />
                  </div>
                  <CardDescription>Real-time risk assessment alerts</CardDescription>
                </CardHeader>
                <CardContent>
                  {riskAlerts.length > 0 ? (
                    <div className="max-h-[400px] overflow-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                            <TableHead>User</TableHead>
                            <TableHead>Risk Level</TableHead>
                            <TableHead>Score</TableHead>
                            <TableHead>Time</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                          {riskAlerts.map((alert, index) => (
                            <TableRow key={`alert-${index}`}>
                              <TableCell>{alert.user_id}</TableCell>
                            <TableCell>
                                <Badge variant={
                                  alert.risk_level === 'high' ? 'destructive' : 
                                  alert.risk_level === 'medium' ? 'secondary' : 'default'
                                }>
                                  {alert.risk_level.toUpperCase()}
                              </Badge>
                            </TableCell>
                              <TableCell>{(alert.risk_score || 0).toFixed(1)}</TableCell>
                              <TableCell>{new Date(alert.timestamp).toLocaleTimeString()}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                              </div>
                  ) : (
                    <Alert>
                      <AlertDescription>No risk alerts received yet.</AlertDescription>
                    </Alert>
                  )}
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>User Activities</CardTitle>
                    <Activity className="h-5 w-5 text-blue-600" />
                              </div>
                  <CardDescription>Real-time user activity stream</CardDescription>
                </CardHeader>
                <CardContent>
                  {realTimeActivities.length > 0 ? (
                    <div className="max-h-[400px] overflow-auto">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>User</TableHead>
                            <TableHead>Activity</TableHead>
                            <TableHead>Time</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {realTimeActivities.map((activity, index) => (
                            <TableRow key={`activity-${index}`}>
                              <TableCell>{activity.user_id}</TableCell>
                              <TableCell>{activity.activity_type}</TableCell>
                              <TableCell>{new Date(activity.timestamp).toLocaleTimeString()}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                  ) : (
                    <Alert>
                      <AlertDescription>No user activities received yet.</AlertDescription>
                    </Alert>
                )}
              </CardContent>
            </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
      
      {/* Session Activity Modal */}
      {showSessionModal && selectedSessionId && (
      <SessionActivityModal
          isOpen={showSessionModal}
          sessionId={selectedSessionId}
        onClose={handleCloseSessionModal}
      />
      )}
    </Layout>
  );
};

export default AdminPage;