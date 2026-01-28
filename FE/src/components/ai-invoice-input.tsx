"use client";

import { useState } from "react";
import { aiInvoiceService, employeeAIInvoiceService } from "@/services/ai-invoice.service";
import { showToast } from "@/components/ui/toast";
import { useRouter } from "next/navigation";
import AIButton from "@/components/ai-button";
import Loader from "@/components/loader";

interface AIInvoiceInputProps {
    role?: "owner" | "employee";
}

export default function AIInvoiceInput({ role = "owner" }: AIInvoiceInputProps) {
    const router = useRouter();
    const [text, setText] = useState("");
    const [loading, setLoading] = useState(false);
    const [isListening, setIsListening] = useState(false);

    const handleSubmit = async () => {
        if (!text.trim()) {
            showToast("Vui lòng nhập lệnh", "error");
            return;
        }

        try {
            setLoading(true);

            // Use correct service based on role
            const service = role === "owner" ? aiInvoiceService : employeeAIInvoiceService;
            const result = await service.createFromText(text);

            // Show warnings if any
            if (result.warnings.length > 0) {
                result.warnings.forEach(w => {
                    showToast(w, "warning");
                });
            }

            // Show confidence warning if low
            if (result.confidence < 0.7) {
                showToast(
                    `⚠️ Độ tin cậy: ${(result.confidence * 100).toFixed(0)}%. Vui lòng kiểm tra kỹ trước khi xác nhận.`,
                    "warning"
                );
            } else {
                showToast(
                    `✓ Độ tin cậy: ${(result.confidence * 100).toFixed(0)}%`,
                    "success"
                );
            }

            showToast("Tạo hóa đơn nháp thành công! Đang chuyển đến chi tiết...", "success");

            // Redirect to invoice detail
            const basePath = role === "owner" ? "/owner" : "/employee";
            router.push(`${basePath}/invoices/${result.invoice.id}`);

        } catch (error: any) {
            const errorMsg = error?.response?.data?.error || error?.message || "Lỗi tạo hóa đơn";
            showToast(errorMsg, "error");
        } finally {
            setLoading(false);
        }
    };

    const handleVoiceInput = () => {
        // Check browser support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            showToast("Trình duyệt không hỗ trợ nhận diện giọng nói", "error");
            return;
        }

        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.lang = 'vi-VN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            setIsListening(true);
            showToast("🎤 Đang lắng nghe... Hãy nói lệnh của bạn", "info");
        };

        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript;
            setText(transcript);
            showToast(`Đã nhận: "${transcript}"`, "success");
        };

        recognition.onerror = (event: any) => {
            setIsListening(false);
            showToast(`Lỗi nhận diện: ${event.error}`, "error");
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        recognition.start();
    };

    return (
        <>
            {loading && <Loader />}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
                <div className="flex items-center gap-3 mb-4">
                    <AIButton
                        onClick={handleSubmit}
                        isLoading={loading}
                        disabled={loading || isListening}
                        size="small"
                    />
                    <div>
                        <h2 className="text-lg font-bold text-[#1e3a8a]">
                            Tạo hóa đơn bằng AI
                        </h2>
                        <p className="text-xs text-slate-500">
                            Nhập lệnh bằng văn bản hoặc giọng nói
                        </p>
                    </div>
                </div>

                <div className="mb-4">
                    <label className="block text-sm font-medium text-[#1e3a8a] mb-2">
                        Lệnh của bạn
                    </label>
                    <textarea
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder='Ví dụ: "Lấy 5 bao xi măng cho anh Ba, ghi nợ" hoặc "Bán 10 cây sắt phi 10 cho chị Lan"'
                        rows={3}
                        disabled={loading || isListening}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent disabled:bg-slate-100"
                    />
                    <p className="text-xs text-slate-500 mt-1">
                        💡 Mẹo: Nói rõ tên sản phẩm, số lượng, khách hàng và cách thanh toán
                    </p>
                </div>

                <div className="flex gap-3">
                    <button
                        onClick={handleSubmit}
                        disabled={loading || isListening || !text.trim()}
                        className="flex-1 px-5 py-2.5 bg-gradient-to-r from-[#00897b] to-[#00695c] text-white rounded-lg text-sm font-bold hover:from-[#007a6c] hover:to-[#00584d] disabled:from-slate-400 disabled:to-slate-400 disabled:cursor-not-allowed transition-all shadow-sm hover:shadow-md"
                    >
                        {loading ? (
                            <span className="flex items-center justify-center gap-2">
                                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                Đang xử lý...
                            </span>
                        ) : (
                            "✨ Tạo hóa đơn"
                        )}
                    </button>

                    <button
                        onClick={handleVoiceInput}
                        disabled={loading || isListening}
                        className={`px-5 py-2.5 rounded-lg text-sm font-bold transition-all shadow-sm hover:shadow-md ${isListening
                            ? "bg-red-500 text-white animate-pulse"
                            : "bg-white border-2 border-[#00897b] text-[#00897b] hover:bg-[#00897b] hover:text-white"
                            } disabled:bg-slate-300 disabled:border-slate-300 disabled:text-slate-600 disabled:cursor-not-allowed`}
                        title="Nhấn để nói (tiếng Việt)"
                    >
                        {isListening ? "🔴 Đang nghe..." : "🎤 Giọng nói"}
                    </button>
                </div>

                {/* Examples */}
                <div className="mt-4 pt-4 border-t border-slate-200">
                    <p className="text-xs font-medium text-slate-600 mb-2">Ví dụ lệnh:</p>
                    <div className="flex flex-wrap gap-2">
                        {[
                            "Lấy 5 bao xi măng cho anh Ba, ghi nợ",
                            "Bán 10 cây sắt phi 10 cho chị Lan",
                            "20 bao xi măng và 5 cây sắt, thanh toán tiền mặt"
                        ].map((example, idx) => (
                            <button
                                key={idx}
                                onClick={() => setText(example)}
                                disabled={loading || isListening}
                                className="px-3 py-1.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-md text-xs text-slate-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {example}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}
    );
}
