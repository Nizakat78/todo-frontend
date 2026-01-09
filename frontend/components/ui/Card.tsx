import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  description?: string;
}

const Card = ({ children, className = '', title, description }: CardProps) => {
  return (
    <div className={`bg-white rounded-2xl shadow-xl overflow-hidden card-elevated ${className}`}>
      {(title || description) && (
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 border-b border-gray-100">
          {title && <h3 className="text-xl font-bold text-gray-800">{title}</h3>}
          {description && <p className="mt-2 text-gray-600">{description}</p>}
        </div>
      )}
      <div className={title || description ? 'p-6' : ''}>
        {children}
      </div>
    </div>
  );
};

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

const CardHeader = ({ children, className = '' }: CardHeaderProps) => {
  return (
    <div className={`bg-gradient-to-r from-blue-50 to-indigo-50 p-6 border-b border-gray-100 ${className}`}>
      {children}
    </div>
  );
};

interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}

const CardContent = ({ children, className = '' }: CardContentProps) => {
  return <div className={`p-6 ${className}`}>{children}</div>;
};

interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
}

const CardFooter = ({ children, className = '' }: CardFooterProps) => {
  return (
    <div className={`bg-gray-50 p-6 border-t border-gray-100 ${className}`}>
      {children}
    </div>
  );
};

Card.Header = CardHeader;
Card.Content = CardContent;
Card.Footer = CardFooter;

export default Card;