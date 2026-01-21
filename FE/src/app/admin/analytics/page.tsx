"use client";

import { useEffect, useState } from "react";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { adminService } from "@/services/admin.service";

export default function AdminAnalyticsPage() {
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    totalUsers: 247,
    newSubscriptions: 38,
    totalRevenue: 0,
    activeHouseholds: 189,
  });

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const [userGrowthData, setUserGrowthData] = useState<number[]>([0, 0, 0, 0, 0, 0, 0]);
  const [monthlySubscriptions, setMonthlySubscriptions] = useState<number[]>([0, 0, 0, 0, 0, 0]);
  const [householdActivity, setHouseholdActivity] = useState<{ active: number[]; inactive: number[] }>({
    active: [0, 0, 0, 0, 0, 0],
    inactive: [0, 0, 0, 0, 0, 0],
  });

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const data = await adminService.getAnalytics();

      setStats({
        totalUsers: data.total_users || 0,
        newSubscriptions: data.new_subscriptions || 0,
        totalRevenue: 0,
        activeHouseholds: data.active_households || 0,
      });

      setUserGrowthData(data.user_growth || [0, 0, 0, 0, 0, 0, 0]);
      setMonthlySubscriptions(data.monthly_subscriptions || [0, 0, 0, 0, 0, 0]);
      setHouseholdActivity(data.household_activity || { active: [0, 0, 0, 0, 0, 0], inactive: [0, 0, 0, 0, 0, 0] });
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải dữ liệu phân tích", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <LoadingOverlay isLoading={loading} message="Đang tải dữ liệu phân tích..." />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Phân tích Nền tảng
          </h1>
        </div>

        <>
          {/* Stats Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            {/* Total Users */}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <p className="text-sm font-normal text-[#4b5563] mb-2">Tổng số người dùng</p>
              <p className="text-[32px] font-bold italic text-[#1e3a8a]">{stats.totalUsers}</p>
            </div>

            {/* New Subscriptions */}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <p className="text-sm font-normal text-[#4b5563] mb-2">Đăng ký mới tháng này</p>
              <p className="text-[32px] font-bold italic text-[#1e3a8a]">{stats.newSubscriptions}</p>
            </div>

            {/* Revenue */}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <p className="text-sm font-normal text-[#4b5563] mb-2">Doanh thu</p>
              <p className="text-[32px] font-bold italic text-[#1e3a8a]">-</p>
            </div>

            {/* Active Households */}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <p className="text-sm font-normal text-[#4b5563] mb-2">Hộ kinh doanh Active</p>
              <p className="text-[32px] font-bold italic text-[#1e3a8a]">{stats.activeHouseholds}</p>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* User Growth Line Chart */}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base font-bold italic text-[#1e3a8a]">
                  Người dùng mới theo thời gian
                </h3>
                <p className="text-xs font-normal text-[#4b5563]">7 ngày qua</p>
              </div>
              <div className="relative h-64">
                <svg className="w-full h-full" viewBox="0 0 500 200" preserveAspectRatio="none">
                  {/* Y-axis labels */}
                  <text x="10" y="195" textAnchor="end" className="text-xs fill-[#1e3a8a]">0</text>
                  <text x="10" y="155" textAnchor="end" className="text-xs fill-[#1e3a8a]">10</text>
                  <text x="10" y="115" textAnchor="end" className="text-xs fill-[#1e3a8a]">20</text>
                  <text x="10" y="75" textAnchor="end" className="text-xs fill-[#1e3a8a]">30</text>
                  <text x="10" y="35" textAnchor="end" className="text-xs fill-[#1e3a8a]">40</text>

                  {/* Grid lines */}
                  <line x1="50" y1="180" x2="500" y2="180" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="140" x2="500" y2="140" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="100" x2="500" y2="100" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="60" x2="500" y2="60" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="20" x2="500" y2="20" stroke="#e5e7eb" strokeWidth="1" />

                  {/* Area fill */}
                  <path
                    d={`M 50 ${180 - (userGrowthData[0] / 40) * 160} 
                          L ${50 + (500 - 50) / 6} ${180 - (userGrowthData[1] / 40) * 160}
                          L ${50 + (500 - 50) / 3} ${180 - (userGrowthData[2] / 40) * 160}
                          L ${50 + (500 - 50) / 2} ${180 - (userGrowthData[3] / 40) * 160}
                          L ${50 + (500 - 50) * 2 / 3} ${180 - (userGrowthData[4] / 40) * 160}
                          L ${50 + (500 - 50) * 5 / 6} ${180 - (userGrowthData[5] / 40) * 160}
                          L 500 ${180 - (userGrowthData[6] / 40) * 160}
                          L 500 180 L 50 180 Z`}
                    fill="#10b981"
                    fillOpacity="0.2"
                  />

                  {/* Line */}
                  <path
                    d={`M 50 ${180 - (userGrowthData[0] / 40) * 160} 
                          L ${50 + (500 - 50) / 6} ${180 - (userGrowthData[1] / 40) * 160}
                          L ${50 + (500 - 50) / 3} ${180 - (userGrowthData[2] / 40) * 160}
                          L ${50 + (500 - 50) / 2} ${180 - (userGrowthData[3] / 40) * 160}
                          L ${50 + (500 - 50) * 2 / 3} ${180 - (userGrowthData[4] / 40) * 160}
                          L ${50 + (500 - 50) * 5 / 6} ${180 - (userGrowthData[5] / 40) * 160}
                          L 500 ${180 - (userGrowthData[6] / 40) * 160}`}
                    fill="none"
                    stroke="#10b981"
                    strokeWidth="2"
                  />

                  {/* Data points */}
                  {userGrowthData.map((value, index) => {
                    const x = 50 + (index * (500 - 50)) / 6;
                    const y = 180 - (value / 40) * 160;
                    return (
                      <circle key={index} cx={x} cy={y} r="4" fill="#10b981" />
                    );
                  })}

                  {/* X-axis labels */}
                  <text x="50" y="195" textAnchor="middle" className="text-xs fill-[#1e3a8a]">07/01</text>
                  <text x={50 + (500 - 50) / 2} y="195" textAnchor="middle" className="text-xs fill-[#1e3a8a]">14/01</text>
                  <text x="500" y="195" textAnchor="middle" className="text-xs fill-[#1e3a8a]">21/01</text>
                </svg>
              </div>
            </div>

            {/* Monthly Subscriptions Bar Chart */}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base font-bold italic text-[#1e3a8a]">
                  Đăng ký mới theo tháng
                </h3>
                <p className="text-xs font-normal text-[#4b5563]">6 tháng qua</p>
              </div>
              <div className="relative h-64">
                <svg className="w-full h-full" viewBox="0 0 500 200" preserveAspectRatio="none">
                  {/* Y-axis labels */}
                  <text x="10" y="195" textAnchor="end" className="text-xs fill-[#1e3a8a]">0</text>
                  <text x="10" y="155" textAnchor="end" className="text-xs fill-[#1e3a8a]">10</text>
                  <text x="10" y="115" textAnchor="end" className="text-xs fill-[#1e3a8a]">20</text>
                  <text x="10" y="75" textAnchor="end" className="text-xs fill-[#1e3a8a]">30</text>
                  <text x="10" y="35" textAnchor="end" className="text-xs fill-[#1e3a8a]">40</text>
                  <text x="10" y="5" textAnchor="end" className="text-xs fill-[#1e3a8a]">50</text>

                  {/* Grid lines */}
                  <line x1="50" y1="180" x2="500" y2="180" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="140" x2="500" y2="140" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="100" x2="500" y2="100" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="60" x2="500" y2="60" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="20" x2="500" y2="20" stroke="#e5e7eb" strokeWidth="1" />

                  {/* Bars */}
                  {monthlySubscriptions.map((value, index) => {
                    const barWidth = 60;
                    const barSpacing = 20;
                    const x = 50 + index * (barWidth + barSpacing) + barSpacing / 2;
                    const barHeight = (value / 50) * 160;
                    const y = 180 - barHeight;
                    const monthLabels = ["T8", "T9", "T10", "T11", "T12", "T1"];

                    return (
                      <g key={index}>
                        <rect
                          x={x}
                          y={y}
                          width={barWidth}
                          height={barHeight}
                          fill="#00897b"
                          rx="2"
                        />
                        <text
                          x={x + barWidth / 2}
                          y={y - 5}
                          textAnchor="middle"
                          className="text-xs font-bold italic fill-[#1e3a8a]"
                        >
                          {value}
                        </text>
                        <text
                          x={x + barWidth / 2}
                          y="195"
                          textAnchor="middle"
                          className="text-xs fill-[#1e3a8a]"
                        >
                          {monthLabels[index]}
                        </text>
                      </g>
                    );
                  })}
                </svg>
              </div>
            </div>

            {/* Revenue Chart */}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <h3 className="text-base font-bold italic text-[#1e3a8a] mb-4">
                Doanh thu theo tháng
              </h3>
              <div className="h-64 flex items-center justify-center">
                <p className="text-sm font-normal text-[#4b5563]">Chưa có dữ liệu</p>
              </div>
            </div>

            {/* Household Activity Chart */}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base font-bold italic text-[#1e3a8a]">
                  Hoạt động hộ kinh doanh
                </h3>
                <p className="text-xs font-normal text-[#4b5563]">6 tháng qua</p>
              </div>
              <div className="relative h-64">
                <svg className="w-full h-full" viewBox="0 0 500 200" preserveAspectRatio="none">
                  {/* Y-axis labels */}
                  <text x="10" y="195" textAnchor="end" className="text-xs fill-[#1e3a8a]">0</text>
                  <text x="10" y="155" textAnchor="end" className="text-xs fill-[#1e3a8a]">50</text>
                  <text x="10" y="115" textAnchor="end" className="text-xs fill-[#1e3a8a]">100</text>
                  <text x="10" y="75" textAnchor="end" className="text-xs fill-[#1e3a8a]">150</text>
                  <text x="10" y="35" textAnchor="end" className="text-xs fill-[#1e3a8a]">200</text>

                  {/* Grid lines */}
                  <line x1="50" y1="180" x2="500" y2="180" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="140" x2="500" y2="140" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="100" x2="500" y2="100" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="60" x2="500" y2="60" stroke="#e5e7eb" strokeWidth="1" />
                  <line x1="50" y1="20" x2="500" y2="20" stroke="#e5e7eb" strokeWidth="1" />

                  {/* Stacked bars */}
                  {householdActivity.active.map((active, index) => {
                    const inactive = householdActivity.inactive[index];
                    const total = active + inactive;
                    const barWidth = 60;
                    const barSpacing = 20;
                    const x = 50 + index * (barWidth + barSpacing) + barSpacing / 2;
                    const activeHeight = (active / 200) * 160;
                    const inactiveHeight = (inactive / 200) * 160;
                    const activeY = 180 - activeHeight - inactiveHeight;
                    const inactiveY = 180 - inactiveHeight;
                    const monthLabels = ["T8", "T9", "T10", "T11", "T12", "T1"];

                    return (
                      <g key={index}>
                        {/* Inactive (bottom) */}
                        <rect
                          x={x}
                          y={inactiveY}
                          width={barWidth}
                          height={inactiveHeight}
                          fill="#00897b"
                          rx="2"
                        />
                        {/* Active (top) */}
                        <rect
                          x={x}
                          y={activeY}
                          width={barWidth}
                          height={activeHeight}
                          fill="#ef4444"
                          rx="2"
                        />
                        <text
                          x={x + barWidth / 2}
                          y="195"
                          textAnchor="middle"
                          className="text-xs fill-[#1e3a8a]"
                        >
                          {monthLabels[index]}
                        </text>
                      </g>
                    );
                  })}
                </svg>
              </div>
              <div className="flex items-center justify-between mt-4">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-[#ef4444] rounded"></div>
                    <p className="text-xs font-normal text-[#1e3a8a]">Active</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-[#00897b] rounded"></div>
                    <p className="text-xs font-normal text-[#1e3a8a]">Inactive</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>

      </div>
    </>
  );
}
