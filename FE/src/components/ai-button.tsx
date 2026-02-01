'use client';

import React, { useState } from 'react';

interface AIButtonProps {
  onClick?: () => void;
  isLoading?: boolean;
  disabled?: boolean;
  size?: 'small' | 'medium' | 'large';
}

const AIButton: React.FC<AIButtonProps> = ({
  onClick,
  isLoading = false,
  disabled = false,
  size = 'medium'
}) => {
  const [isHovering, setIsHovering] = useState(false);

  const sizeConfig = {
    small: { width: 80, height: 80, iconSize: 40 },
    medium: { width: 120, height: 120, iconSize: 54 },
    large: { width: 142, height: 142, iconSize: 64 }
  };

  const config = sizeConfig[size];

  return (
    <div className="relative group perspective-1000">
      <style jsx>{`
        @keyframes spin-and-zoom {
          0% { transform: rotate(0deg) scale(1); }
          50% { transform: rotate(180deg) scale(1.1); }
          100% { transform: rotate(360deg) scale(1); }
        }
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          50% { opacity: 1; }
          100% { transform: translateX(100%); opacity: 0; }
        }
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-spin-and-zoom {
          animation: spin-and-zoom 2s cubic-bezier(0.25, 0.8, 0.25, 1) infinite;
        }
        .animate-shimmer {
          animation: shimmer 2s infinite;
        }
        .animate-fade-in-up {
          animation: fadeInUp 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
        }
      `}</style>

      <button
        onClick={onClick}
        disabled={disabled || isLoading}
        onMouseEnter={() => setIsHovering(true)}
        onMouseLeave={() => setIsHovering(false)}
        style={{ width: config.width, height: config.height }}
        className={`
          flex flex-col items-center justify-center
          bg-[#063525] border-[3px] border-[#42c498] rounded-xl
          text-[#e5dede] font-bold relative cursor-pointer overflow-hidden
          transition-all duration-300 ease-[cubic-bezier(0.25,0.8,0.25,1)]
          shadow-[4px_4px_1px_#000000] p-0
          disabled:opacity-60 disabled:cursor-not-allowed disabled:bg-[#0a3d2e]
          hover:disabled:bg-[#0a3d2e] hover:disabled:transform-none hover:disabled:shadow-[4px_4px_1px_#000000] hover:disabled:border-[#42c498]
          hover:bg-[#1a5c46] hover:border-[#030504]
          hover:-translate-x-1.5 hover:-translate-y-1.5 hover:rotate-1
          hover:shadow-[10px_10px_0_#000000,15px_15px_20px_rgba(64,164,122,0.2)]
          active:translate-x-[-2px] active:translate-y-[-2px]
        `}
      >
        <div className="flex flex-col items-center justify-center w-full h-full z-[2] relative">
          <div
            className={`
              flex items-center justify-center transition-all duration-300 ease-[cubic-bezier(0.25,0.8,0.25,1)] text-[#42c498]
              ${isHovering ? '-translate-y-2 text-[#5cdbab]' : ''}
              ${isHovering && isLoading ? 'animate-spin-and-zoom' : ''}
            `}
          >
            <svg
              className={`
                transition-all duration-300 ease-[cubic-bezier(0.25,0.8,0.25,1)] drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]
                ${isLoading ? 'animate-spin' : ''}
                ${isHovering ? 'drop-shadow-[0_4px_8px_rgba(66,196,152,0.4)]' : ''}
              `}
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              width={config.iconSize}
              height={config.iconSize}
            >
              <path
                d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.8956zm16.0993 3.8558L12.5907 8.3829 14.6108 7.2144a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.3927-.6813zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z"
                fill="currentColor"
              />
            </svg>
          </div>

          {isHovering && (
            <div className="flex flex-col items-center text-center leading-[1.2] animate-fade-in-up">
              <span className="text-[10px] font-normal tracking-[0.5px] text-[#a8a8a8] mt-1">
                Powered By
              </span>
              <span className="text-[12px] font-bold tracking-[0.5px] text-[#42c498] mt-[2px] drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]">
                GPT-Omni
              </span>
            </div>
          )}
        </div>

        {/* Shine effect pseudo-elements */}
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-transparent via-[rgba(255,255,255,0.1)] to-transparent pointer-events-none animate-shimmer" />
      </button>
    </div>
  );
};

export default AIButton;
