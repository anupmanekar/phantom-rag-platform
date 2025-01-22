"use client";
import React, { useState } from 'react';
import Chat from './Chat';

interface ChatWindowProps {
  onClose: () => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ onClose }) => {
  return (
    <div className="bottom-0 right-0 w-1/2 h-auto bg-white shadow-lg border border-gray-300 rounded-lg overflow-hidden">
      <div className="flex justify-between items-center p-2 bg-gray-100 border-b border-gray-300">
        <h2 className="text-lg font-semibold">Chat</h2>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-700 focus:outline-none">
          ✖
        </button>
      </div>
      <div className="p-2">
        <Chat />
      </div>
    </div>
  );
};

export default ChatWindow;
