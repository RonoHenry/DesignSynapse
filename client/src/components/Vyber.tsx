import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, X, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const Vyber = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm Vyber, your AI design assistant. How can I help you with your project today?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const newMessage = {
      id: messages.length + 1,
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');

    // Simulate bot response
    setTimeout(() => {
      const botResponse = {
        id: messages.length + 2,
        text: "I understand you're looking for assistance with your design project. Let me help you explore the possibilities with Design Synapse!",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <div className="fixed bottom-6 right-6 z-50">
        {!isOpen && (
          <Button
            onClick={() => setIsOpen(true)}
            className="w-16 h-16 rounded-full synapse-gradient shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110 animate-pulse"
          >
            <div className="relative">
              <MessageCircle className="w-8 h-8 text-white" />
              <Sparkles className="w-4 h-4 text-white absolute -top-1 -right-1 animate-bounce" />
            </div>
          </Button>
        )}

        {/* Chat Window */}
        {isOpen && (
          <div className="w-96 h-[500px] bg-white dark:bg-gray-900 custom:bg-gradient-to-br custom:from-purple-900/95 custom:to-indigo-900/95 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 custom:border-purple-500/30 backdrop-blur-sm animate-scale-in flex flex-col overflow-hidden">
            {/* Header */}
            <div className="p-4 synapse-gradient text-white flex items-center justify-between rounded-t-2xl">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Vyber</h3>
                  <p className="text-xs opacity-90">AI Design Assistant</p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsOpen(false)}
                className="text-white hover:bg-white/20 w-8 h-8"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>

            {/* Messages */}
            <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-gray-50 dark:bg-gray-800 custom:bg-purple-900/20">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-2xl ${
                      message.sender === 'user'
                        ? 'synapse-gradient text-white rounded-br-md'
                        : 'bg-white dark:bg-gray-700 custom:bg-purple-800/50 text-gray-800 dark:text-white custom:text-white rounded-bl-md border dark:border-gray-600 custom:border-purple-500/30'
                    } animate-fade-in`}
                  >
                    <p className="text-sm">{message.text}</p>
                    <p className={`text-xs mt-1 opacity-70 ${
                      message.sender === 'user' ? 'text-white/70' : 'text-gray-500 dark:text-gray-400 custom:text-purple-200'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 bg-white dark:bg-gray-900 custom:bg-purple-900/30 border-t border-gray-200 dark:border-gray-700 custom:border-purple-500/30 rounded-b-2xl">
              <div className="flex space-x-2">
                <Input
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything about your project..."
                  className="flex-1 bg-gray-50 dark:bg-gray-800 custom:bg-purple-800/50 border-0 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 custom:focus:ring-purple-400 dark:text-white custom:text-white custom:placeholder:text-purple-200"
                />
                <Button
                  onClick={handleSendMessage}
                  className="synapse-gradient hover:scale-105 transition-transform w-10 h-10 p-0"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Floating Animation Dots */}
      {!isOpen && (
        <div className="fixed bottom-6 right-6 z-40 pointer-events-none">
          <div className="absolute inset-0 animate-ping">
            <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-400 to-teal-400 opacity-20"></div>
          </div>
          <div className="absolute inset-2 animate-pulse delay-75">
            <div className="w-12 h-12 rounded-full bg-gradient-to-r from-teal-400 to-orange-400 opacity-30"></div>
          </div>
        </div>
      )}
    </>
  );
};

export default Vyber;
