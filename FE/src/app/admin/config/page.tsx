"use client";

export default function AdminConfigPage() {
  const upcomingFeatures = [
    "Cấu hình templates báo cáo tài chính (Circular 88/2021/TT-BTC)",
    "Quản lý thông báo toàn hệ thống",
    "Cài đặt email và thông báo tự động",
    "Cấu hình backup và bảo mật dữ liệu",
    "Quản lý logs và theo dõi hoạt động hệ thống",
    "Tùy chỉnh giao diện và branding",
  ];

  return (
    <div className="p-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
          Cài đặt Hệ thống
        </h1>
        <p className="text-[15px] font-normal text-[#4b5563]">
          Cấu hình và quản lý các thiết lập toàn hệ thống
        </p>
      </div>

      {/* Placeholder Card */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12">
        <div className="flex flex-col items-center text-center max-w-3xl mx-auto">
          {/* Icon */}
          <div className="mb-6">
            <div className="w-24 h-24 bg-[#e0f2f1] rounded-full flex items-center justify-center">
              <svg
                className="w-12 h-12 text-[#00897b]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
            </div>
          </div>

          {/* Title */}
          <h2 className="text-[24px] font-bold italic text-[#1e3a8a] mb-4">
            Chức năng đang phát triển
          </h2>

          {/* Description */}
          <div className="mb-8 text-[16px] font-normal text-[#4b5563] leading-relaxed">
            <p className="mb-2">
              Trang Cài đặt Hệ thống đang được xây dựng. Các tính năng sẽ sớm được ra mắt để giúp bạn
            </p>
            <p>
              quản lý và tùy chỉnh hệ thống BizFlow một cách toàn diện.
            </p>
          </div>

          {/* Feature List Card */}
          <div className="w-full bg-slate-50 rounded-lg border border-slate-200 p-6 mb-8">
            <h3 className="text-[16px] font-bold italic text-[#1e3a8a] mb-4 text-left">
              Các tính năng sắp ra mắt:
            </h3>
            <ul className="space-y-3 text-left">
              {upcomingFeatures.map((feature, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="mt-1 flex-shrink-0">
                    <svg
                      className="w-5 h-5 text-[#10b981]"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <p className="text-[15px] font-normal text-[#4b5563] flex-1">
                    {feature}
                  </p>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Link */}
          <div className="flex items-center gap-2 text-[#00897b]">
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
            <p className="text-[15px] font-normal">
              Liên hệ để biết thêm chi tiết về lộ trình phát triển
            </p>
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
