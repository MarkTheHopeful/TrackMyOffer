import { cn } from '@/lib/utils';
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'accent';
  size?: 'sm' | 'md' | 'lg';
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', ...props }, ref) => {
    return (
      <button
        className={cn(
          'inline-flex items-center justify-center rounded-lg font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
          {
            'bg-gradient-to-r from-brand-600 to-brand-500 text-white shadow-lg shadow-brand-500/25 hover:shadow-brand-500/40': variant === 'primary',
            'bg-white text-slate-900 shadow-lg shadow-slate-200/50 border border-slate-200 hover:border-brand-300 hover:shadow-brand-100/50': variant === 'secondary',
            'text-slate-600 hover:text-brand-600 hover:bg-brand-50': variant === 'ghost',
            'bg-gradient-to-r from-accent-600 to-accent-500 text-white shadow-lg shadow-accent-500/25 hover:shadow-accent-500/40': variant === 'accent',
            'h-8 px-3 text-sm': size === 'sm',
            'h-10 px-4': size === 'md',
            'h-12 px-6 text-lg': size === 'lg',
          },
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';