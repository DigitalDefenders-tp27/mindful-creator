/**
 * 合并多个类名字符串
 * @param classes 要合并的类名
 * @returns 合并后的类名字符串
 */
export function cn(...classes: any[]): string {
  return classes.filter(Boolean).join(' ');
} 