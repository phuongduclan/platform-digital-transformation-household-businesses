"use client";

import { useEffect, useState } from "react";
import { initializeSocket, getSocket, disconnectSocket } from "@/lib/socket";
import { showToast } from "@/components/ui/toast";
import { useRouter } from "next/navigation";

interface Notification {
    type: string;
    timestamp: string;
    data: {
        invoice_id: number;
        invoice: any;
        confidence: number;
        warnings: string[];
        household_id: number;
    };
}

interface NotificationBellProps {
    householdId: number;
    role: "owner" | "employee";
}

export default function NotificationBell({ householdId, role }: NotificationBellProps) {
    const router = useRouter();
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        if (!householdId) return;

        // Initialize socket connection
        const socket = initializeSocket(householdId);

        // Listen for notifications
        socket.on('notification', (notification: Notification) => {
            console.log('Received notification:', notification);

            // Add to notifications list
            setNotifications(prev => [notification, ...prev]);
            setUnreadCount(prev => prev + 1);

            // Show toast for AI draft created
            if (notification.type === 'ai_draft_created') {
                const invoiceId = notification.data.invoice_id;
                const confidence = notification.data.confidence;

                showToast(
                    `🤖 AI đã tạo hóa đơn nháp #${invoiceId} (Độ tin cậy: ${(confidence * 100).toFixed(0)}%)`,
                    confidence >= 0.7 ? "success" : "warning"
                );
            }
        });

        // Cleanup on unmount
        return () => {
            disconnectSocket();
        };
    }, [householdId]);

    const handleNotificationClick = (notification: Notification) => {
        if (notification.type === 'ai_draft_created') {
            const invoiceId = notification.data.invoice_id;
            const basePath = role === "owner" ? "/owner" : "/employee";
            router.push(`${basePath}/invoices/${invoiceId}`);
            setIsOpen(false);
        }
    };

    const clearAllNotifications = () => {
        setNotifications([]);
        setUnreadCount(0);
    };

    return (
        <div className="relative">
            {/* Bell Icon */}
            <button
                onClick={() => {
                    setIsOpen(!isOpen);
                    if (!isOpen) setUnreadCount(0);
                }}
                className="relative p-2 text-[#1e3a8a] hover:bg-slate-100 rounded-lg transition-colors"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={2}
                    stroke="currentColor"
                    className="w-6 h-6"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"
                    />
                </svg>
                {unreadCount > 0 && (
                    <span className="absolute top-0 right-0 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-500 rounded-full min-w-[20px]">
                        {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                )}
            </button>

            {/* Notification Dropdown */}
            {isOpen && (
                <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-slate-200 z-50">
                    <div className="flex items-center justify-between px-4 py-3 border-b border-slate-200">
                        <h3 className="text-sm font-bold text-[#1e3a8a]">Thông báo</h3>
                        {notifications.length > 0 && (
                            <button
                                onClick={clearAllNotifications}
                                className="text-xs text-[#00897b] hover:underline"
                            >
                                Xóa tất cả
                            </button>
                        )}
                    </div>

                    <div className="max-h-96 overflow-y-auto">
                        {notifications.length === 0 ? (
                            <div className="px-4 py-8 text-center text-sm text-slate-500">
                                Không có thông báo mới
                            </div>
                        ) : (
                            notifications.map((notif, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => handleNotificationClick(notif)}
                                    className="w-full px-4 py-3 hover:bg-slate-50 border-b border-slate-100 text-left transition-colors"
                                >
                                    {notif.type === 'ai_draft_created' && (
                                        <div>
                                            <div className="flex items-start gap-2">
                                                <span className="text-lg">🤖</span>
                                                <div className="flex-1">
                                                    <p className="text-sm font-medium text-[#1e3a8a]">
                                                        AI tạo hóa đơn nháp #{notif.data.invoice_id}
                                                    </p>
                                                    <p className="text-xs text-slate-500 mt-1">
                                                        Độ tin cậy: {(notif.data.confidence * 100).toFixed(0)}%
                                                    </p>
                                                    {notif.data.warnings.length > 0 && (
                                                        <p className="text-xs text-orange-600 mt-1">
                                                            ⚠️ {notif.data.warnings.length} cảnh báo
                                                        </p>
                                                    )}
                                                    <p className="text-xs text-slate-400 mt-1">
                                                        {new Date(notif.timestamp).toLocaleString('vi-VN')}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </button>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
