import { Layout } from '@/components/layout/Layout';
import { useAuth } from '@/hooks/useAuth';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { BarChart3, Settings, User, TrendingUp } from 'lucide-react';

const hardcodedSessions = [
  {
    date: '2025-07-08 18:04:09',
    productsViewed: 14,
    cartActions: 4,
    wishlistActions: 0,
    categoryChanges: 0,
    searches: 0,
    lastVisited: '2025-07-08 18:04:09',
  },
  {
    date: '2025-07-08 16:22:41',
    productsViewed: 8,
    cartActions: 2,
    wishlistActions: 1,
    categoryChanges: 3,
    searches: 2,
    lastVisited: '2025-07-08 16:22:41',
  },
];

const UserActivity = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">User Activity</h1>
          <p className="text-muted-foreground">
            Welcome back, {user?.name || user?.email}!
          </p>
        </div>

        {/* Dashboard Cards */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card
            className="cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => handleNavigate('/profile')}
          >
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

          <Card
            className="cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => handleNavigate('/admin')}
          >
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

          <Card
            className="cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => handleNavigate('/settings')}
          >
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

        {/* Quick Stats Section */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Total Sessions</CardDescription>
              <CardTitle className="text-2xl">24</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                +12% from last month
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Avg. Session Time</CardDescription>
              <CardTitle className="text-2xl">45m</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                +5% from last week
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Tasks Completed</CardDescription>
              <CardTitle className="text-2xl">152</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                +18% from last month
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Success Rate</CardDescription>
              <CardTitle className="text-2xl">98%</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                +2% from last month
              </p>
            </CardContent>
          </Card>
        </div>

        {/* User Activity Table */}
        <div>
          <h2 className="text-xl font-semibold mt-8 mb-4">Recent Activity</h2>
          <div className="overflow-x-auto rounded-lg border">
            <table className="min-w-full bg-white text-sm">
              <thead>
                <tr className="bg-gray-50 text-gray-700">
                  <th className="px-4 py-2 text-left">Session Date</th>
                  <th className="px-4 py-2 text-left">Products Viewed</th>
                  <th className="px-4 py-2 text-left">Cart Actions</th>
                  <th className="px-4 py-2 text-left">Wishlist Actions</th>
                  <th className="px-4 py-2 text-left">Category Changes</th>
                  <th className="px-4 py-2 text-left">Searches</th>
                  <th className="px-4 py-2 text-left">Last Visited</th>
                </tr>
              </thead>
              <tbody>
                {hardcodedSessions.map((session, idx) => (
                  <tr key={idx} className="border-t">
                    <td className="px-4 py-2">{session.date}</td>
                    <td className="px-4 py-2">{session.productsViewed}</td>
                    <td className="px-4 py-2">{session.cartActions}</td>
                    <td className="px-4 py-2">{session.wishlistActions}</td>
                    <td className="px-4 py-2">{session.categoryChanges}</td>
                    <td className="px-4 py-2">{session.searches}</td>
                    <td className="px-4 py-2">{session.lastVisited}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default UserActivity;