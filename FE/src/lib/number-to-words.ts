/**
 * Convert number to Vietnamese words
 * Example: 5329500 → "Năm triệu ba trăm hai mươi chín nghìn năm trăm đồng chẵn"
 */

const ones = ['', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín'];
const teens = ['mười', 'mười một', 'mười hai', 'mười ba', 'mười bốn', 'mười lăm', 'mười sáu', 'mười bảy', 'mười tám', 'mười chín'];
const tens = ['', 'mười', 'hai mươi', 'ba mươi', 'bốn mươi', 'năm mươi', 'sáu mươi', 'bảy mươi', 'tám mươi', 'chín mươi'];

function convertThreeDigits(num: number): string {
    if (num === 0) return '';
    
    const hundred = Math.floor(num / 100);
    const remainder = num % 100;
    const ten = Math.floor(remainder / 10);
    const one = remainder % 10;
    
    let result = '';
    
    // Hàng trăm
    if (hundred > 0) {
        result += ones[hundred] + ' trăm';
        if (remainder > 0) result += ' ';
    }
    
    // Hàng chục
    if (ten === 0 && one > 0 && hundred > 0) {
        result += 'lẻ ';
    }
    
    if (ten === 1) {
        result += teens[one];
    } else if (ten > 1) {
        result += tens[ten];
        if (one > 0) {
            if (one === 1 && ten > 1) {
                result += ' mốt';
            } else if (one === 5 && ten > 1) {
                result += ' lăm';
            } else {
                result += ' ' + ones[one];
            }
        }
    } else if (one > 0 && ten === 0) {
        result += ones[one];
    }
    
    return result.trim();
}

export function numberToVietnameseWords(num: number): string {
    if (num === 0) return 'Không đồng';
    
    // Round to integer
    num = Math.round(num);
    
    if (num < 0) return 'Số âm không hợp lệ';
    if (num > 999999999999) return 'Số quá lớn';
    
    const billion = Math.floor(num / 1000000000);
    const million = Math.floor((num % 1000000000) / 1000000);
    const thousand = Math.floor((num % 1000000) / 1000);
    const hundred = num % 1000;
    
    let result = '';
    
    if (billion > 0) {
        result += convertThreeDigits(billion) + ' tỷ';
        if (million > 0 || thousand > 0 || hundred > 0) result += ' ';
    }
    
    if (million > 0) {
        result += convertThreeDigits(million) + ' triệu';
        if (thousand > 0 || hundred > 0) result += ' ';
    }
    
    if (thousand > 0) {
        result += convertThreeDigits(thousand) + ' nghìn';
        if (hundred > 0) result += ' ';
    }
    
    if (hundred > 0) {
        result += convertThreeDigits(hundred);
    }
    
    // Capitalize first letter
    result = result.charAt(0).toUpperCase() + result.slice(1);
    
    // Add "đồng chẵn" or "đồng"
    if (num % 1000 === 0) {
        result += ' đồng chẵn';
    } else {
        result += ' đồng';
    }
    
    return result.trim();
}
