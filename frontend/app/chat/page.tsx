import { useState } from "react";
import ChatIcon from "@/app/components/ChatIcon";
import ChatWindow from "@/app/components/ChatWindow";

const ChatPage = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleChatIconClick = () => {
    setIsChatOpen(true);
  };

  const handleChatWindowClose = () => {
    setIsChatOpen(false);
  };

  return (
    <div>
      <ChatIcon onClick={handleChatIconClick} />
      {isChatOpen && <ChatWindow onClose={handleChatWindowClose} />}
    </div>
  );
};

export default ChatPage;
