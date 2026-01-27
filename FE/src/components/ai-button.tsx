'use client';

import React, { useState } from 'react';
import styled from 'styled-components';

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
    <StyledWrapper $size={size}>
      <button
        className="ai-button"
        onClick={onClick}
        disabled={disabled || isLoading}
        onMouseEnter={() => setIsHovering(true)}
        onMouseLeave={() => setIsHovering(false)}
      >
        <div className="ai-content">
          <div className="ai-logo-container">
            <svg
              className={`ai-icon ${isLoading ? 'spinning' : ''}`}
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
            <div className="button-text">
              <span className="text-powered-by">Powered By</span>
              <span className="text-gpt">GPT-Omni</span>
            </div>
          )}
        </div>

        {/* Shine effect pseudo-elements */}
        <div className="shine-effect" />
      </button>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div<{ $size: 'small' | 'medium' | 'large' }>`
  ${props => {
    const sizes = {
      small: { width: 80, height: 80 },
      medium: { width: 120, height: 120 },
      large: { width: 142, height: 142 }
    };
    const size = sizes[props.$size];
    return `
      .ai-button {
        width: ${size.width}px;
        height: ${size.height}px;
      }
    `;
  }}

  .ai-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #063525;
    border: 3px solid #42c498;
    border-radius: 12px;
    color: #e5dede;
    font-weight: bold;
    position: relative;
    cursor: pointer;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 4px 4px 1px #000000;
    padding: 0;

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      background-color: #0a3d2e;
    }

    &:hover:not(:disabled) {
      background-color: #1a5c46;
      border-color: #030504;
      transform: translate(-6px, -6px) rotate(1deg);
      box-shadow: 10px 10px 0 #000000, 15px 15px 20px rgba(64, 164, 122, 0.2);
    }

    &:active:not(:disabled) {
      transform: translate(-2px, -2px);
    }
  }

  .ai-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    z-index: 2;
    position: relative;
  }

  .ai-logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    color: #42c498;

    .ai-button:hover & {
      transform: translateY(-8px);
      color: #5cdbab;
    }

    .ai-button:hover &.spinning {
      animation: spin-and-zoom 2s cubic-bezier(0.25, 0.8, 0.25, 1) infinite;
    }
  }

  .ai-icon {
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));

    .ai-button:hover & {
      filter: drop-shadow(0 4px 8px rgba(66, 196, 152, 0.4));
    }
  }

  .button-text {
    display: flex;
    flex-direction: column;
    align-items: center;
    line-height: 1.2;
    text-align: center;
    animation: fadeInUp 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
  }

  .text-powered-by {
    font-size: 10px;
    font-weight: normal;
    letter-spacing: 0.5px;
    color: #a8a8a8;
    margin-top: 4px;
  }

  .text-gpt {
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 0.5px;
    color: #42c498;
    margin-top: 2px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .shine-effect {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.1),
      transparent
    );
    animation: shimmer 2s infinite;
    pointer-events: none;
  }

  @keyframes spin-and-zoom {
    0% {
      transform: rotate(0deg) scale(1);
    }
    50% {
      transform: rotate(180deg) scale(1.1);
    }
    100% {
      transform: rotate(360deg) scale(1);
    }
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes shimmer {
    0% {
      transform: translateX(-100%);
    }
    50% {
      opacity: 1;
    }
    100% {
      transform: translateX(100%);
      opacity: 0;
    }
  }

  @keyframes spinning {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  .spinning {
    animation: spinning 2s linear infinite !important;
  }
`;

export default AIButton;
