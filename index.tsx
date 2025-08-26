// pages/index.tsx - Landing page

import React from 'react';
import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>AI SaaS Platform - Advanced AI Tools for Everyone</title>
        <meta name="description" content="Powerful AI tools for text generation, image creation, code generation, and content summarization." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
        {/* Navigation */}
        <nav className="bg-white/80 backdrop-blur-sm dark:bg-gray-900/80 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  🤖 AI Platform
                </h1>
              </div>
              <div className="flex items-center space-x-4">
                <a href="/auth/login" className="btn btn-outline">
                  Login
                </a>
                <a href="/auth/register" className="btn btn-primary">
                  Sign Up
                </a>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              Supercharge Your Workflow with{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                AI Tools
              </span>
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              Generate text, create images, write code, and summarize content with our powerful AI platform. 
              Everything you need to boost productivity in one place.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="/auth/register" className="btn btn-primary text-lg px-8 py-3">
                Get Started Free
              </a>
              <a href="#features" className="btn btn-outline text-lg px-8 py-3">
                Learn More
              </a>
            </div>
          </div>

          {/* Features Section */}
          <section id="features" className="mt-32">
            <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-16">
              Powerful AI Tools at Your Fingertips
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              <div className="card p-6 text-center">
                <div className="text-4xl mb-4">📝</div>
                <h3 className="text-xl font-semibold mb-2">Text Generation</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Generate high-quality content, articles, and copy using advanced language models.
                </p>
              </div>
              <div className="card p-6 text-center">
                <div className="text-4xl mb-4">🎨</div>
                <h3 className="text-xl font-semibold mb-2">Image Creation</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Create stunning visuals and artwork from simple text descriptions.
                </p>
              </div>
              <div className="card p-6 text-center">
                <div className="text-4xl mb-4">💻</div>
                <h3 className="text-xl font-semibold mb-2">Code Generation</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Generate, debug, and optimize code in multiple programming languages.
                </p>
              </div>
              <div className="card p-6 text-center">
                <div className="text-4xl mb-4">📊</div>
                <h3 className="text-xl font-semibold mb-2">Content Summarization</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Quickly summarize long documents, articles, and research papers.
                </p>
              </div>
            </div>
          </section>

          {/* Pricing Section */}
          <section className="mt-32">
            <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-16">
              Simple, Transparent Pricing
            </h2>
            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              <div className="card p-8">
                <h3 className="text-2xl font-bold mb-4">Starter</h3>
                <div className="text-4xl font-bold mb-4">$9<span className="text-lg text-gray-500">/month</span></div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    1,000 AI credits/month
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Basic text generation
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Email support
                  </li>
                </ul>
                <button className="btn btn-outline w-full">Get Started</button>
              </div>
              <div className="card p-8 border-primary-500 relative">
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-primary-500 text-white px-3 py-1 rounded-full text-sm">Most Popular</span>
                </div>
                <h3 className="text-2xl font-bold mb-4">Professional</h3>
                <div className="text-4xl font-bold mb-4">$29<span className="text-lg text-gray-500">/month</span></div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    10,000 AI credits/month
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    All AI tools access
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Priority support
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    API access
                  </li>
                </ul>
                <button className="btn btn-primary w-full">Get Started</button>
              </div>
              <div className="card p-8">
                <h3 className="text-2xl font-bold mb-4">Enterprise</h3>
                <div className="text-4xl font-bold mb-4">$99<span className="text-lg text-gray-500">/month</span></div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Unlimited AI credits
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Custom AI models
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    24/7 phone support
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Team collaboration
                  </li>
                </ul>
                <button className="btn btn-outline w-full">Contact Sales</button>
              </div>
            </div>
          </section>
        </main>

        {/* Footer */}
        <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 mt-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                🤖 AI Platform
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Built with Next.js, TypeScript, and TailwindCSS
              </p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}