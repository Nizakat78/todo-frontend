'use client';

import React from 'react';
import { useAuth } from '../hooks/useAuth';
import Link from 'next/link';
import Button from '../components/ui/Button';

const HomePage = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 left-0 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
        <div className="absolute top-0 right-0 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow animation-delay-2000"></div>
        <div className="absolute bottom-0 left-1/2 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow animation-delay-4000"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-24 mx-auto max-w-7xl px-4 sm:mt-28 sm:px-6 md:mt-32 lg:mt-36 lg:px-8 xl:mt-40">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl lg:text-7xl">
                  <span className="block">Manage your tasks</span>{' '}
                  <span className="block bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                    with ease
                  </span>
                </h1>
                <p className="mt-6 text-base text-gray-600 sm:mt-8 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-10 md:text-xl lg:mx-0">
                  A beautiful and intuitive todo application to help you organize your daily tasks and boost productivity.
                  Stay focused, get things done, and achieve your goals.
                </p>
                <div className="mt-10 sm:mt-12 sm:flex sm:justify-center lg:justify-start space-y-4 sm:space-y-0 sm:space-x-6">
                  {!isAuthenticated ? (
                    <div className="rounded-xl shadow-xl transform transition-all duration-300 hover:scale-105">
                      <Link href="/signup">
                        <Button variant="primary" size="lg" className="text-lg px-8 py-4 rounded-xl">
                          <svg className="mr-3 h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                          </svg>
                          Get Started Free
                        </Button>
                      </Link>
                    </div>
                  ) : (
                    <div className="rounded-xl shadow-xl transform transition-all duration-300 hover:scale-105">
                      <Link href="/dashboard">
                        <Button variant="primary" size="lg" className="text-lg px-8 py-4 rounded-xl">
                          <svg className="mr-3 h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                          </svg>
                          Go to Dashboard
                        </Button>
                      </Link>
                    </div>
                  )}
                  <div className="mt-4 sm:mt-0">
                    <Link href="/login">
                      <Button variant="ghost" size="lg" className="text-lg px-8 py-4 rounded-xl text-gray-700 hover:text-blue-600">
                        {isAuthenticated ? (
                          <>
                            <svg className="mr-3 h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            View Profile
                          </>
                        ) : (
                          <>
                            <svg className="mr-3 h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                            </svg>
                            Sign In
                          </>
                        )}
                      </Button>
                    </Link>
                  </div>
                </div>

                {/* Feature highlights */}
                <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-4xl mx-auto">
                  <div className="text-center p-6 bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg">
                    <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900">Organize Tasks</h3>
                    <p className="mt-2 text-gray-600">Easily create, update, and manage your tasks with our intuitive interface.</p>
                  </div>

                  <div className="text-center p-6 bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg">
                    <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900">Track Progress</h3>
                    <p className="mt-2 text-gray-600">Monitor your progress with visual indicators and completion statistics.</p>
                  </div>

                  <div className="text-center p-6 bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg">
                    <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900">Secure & Private</h3>
                    <p className="mt-2 text-gray-600">Your data is securely stored and protected with industry-standard encryption.</p>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;