# 使用 Node.js 18 作為基礎映像
FROM node:18-slim

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 tools/package.json
COPY tools/package.json tools/
COPY package.json .

# 安裝依賴
WORKDIR /app/tools
RUN npm install

# 複製其他文件
WORKDIR /app
COPY . .

# 設定環境變數
ENV NODE_ENV=production

# 暴露 WebSocket 端口（3000）
EXPOSE 3000

# 設定容器啟動命令
CMD ["node", "tools/subscribe-data.js"]