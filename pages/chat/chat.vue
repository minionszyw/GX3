<template>
	<view class="container">
		<!-- 消息展示区域 -->
		<scroll-view class="message-container" scroll-y="true" :scroll-top="scrollTop">
			<view v-for="(message, index) in messages" :key="index" class="message-item">
				<!-- 用户消息 -->
				<view v-if="message.role === 'user'" class="user-message">
					<view class="message-bubble user-bubble">
						<text class="message-text">{{ message.content }}</text>
					</view>
					<image class="avatar" src="/static/user-avatar.png" mode="aspectFill"></image>
				</view>
				
				<!-- AI回复 -->
				<view v-else class="ai-message">
					<image class="avatar" src="/static/ai-avatar.png" mode="aspectFill"></image>
					<view class="message-bubble ai-bubble">
						<text class="message-text">{{ message.content }}</text>
					</view>
				</view>
				
				<!-- 时间戳 -->
				<view v-if="showTimestamp(index)" class="timestamp">
					{{ formatTime(message.timestamp) }}
				</view>
			</view>
		</scroll-view>
		
		<!-- 输入控制区域 -->
		<view class="input-container">
			<view class="input-actions">
				<button class="action-btn" @click="createNewSession">新建会话</button>
				<button class="action-btn" @click="clearHistory">清空记录</button>
			</view>
			<view class="input-area">
				<input class="message-input" v-model="inputMessage" placeholder="请输入您的问题..." @confirm="sendMessage" />
				<button class="send-btn" @click="sendMessage" :disabled="!inputMessage || isSending">发送</button>
			</view>
		</view>
	</view>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useChatStore } from '@/store/chat/chat'

export default {
	data() {
		return {
			inputMessage: '',
			scrollTop: 0,
			isSending: false
		}
	},
	
	computed: {
		...mapState(useChatStore, ['messages', 'currentSession'])
	},
	
	onLoad() {
		// 页面加载时初始化聊天
		this.initChat()
	},
	
	methods: {
		...mapActions(useChatStore, ['sendMessage', 'createSession', 'clearMessages']),
		
		async initChat() {
			// 初始化聊天会话
			if (!this.currentSession) {
				await this.createSession()
			}
		},
		
		async sendMessage() {
			if (!this.inputMessage.trim() || this.isSending) return
			
			this.isSending = true
			const message = this.inputMessage.trim()
			this.inputMessage = ''
			
			try {
				await this.sendMessage(message)
				// 滚动到底部
				this.$nextTick(() => {
					this.scrollTop = 999999
				})
			} catch (error) {
				console.error('发送消息失败:', error)
				uni.showToast({
					title: '发送失败，请重试',
					icon: 'none'
				})
			} finally {
				this.isSending = false
			}
		},
		
		createNewSession() {
			uni.showModal({
				title: '新建会话',
				content: '确定要新建会话吗？当前会话内容将被保存。',
				success: (res) => {
					if (res.confirm) {
						this.createSession()
						uni.showToast({
							title: '已创建新会话',
							icon: 'success'
						})
					}
				}
			})
		},
		
		clearHistory() {
			uni.showModal({
				title: '清空记录',
				content: '确定要清空当前会话记录吗？此操作不可恢复。',
				success: (res) => {
					if (res.confirm) {
						this.clearMessages()
						uni.showToast({
							title: '已清空记录',
							icon: 'success'
						})
					}
				}
			})
		},
		
		showTimestamp(index) {
			// 控制时间戳显示逻辑
			if (index === 0) return true
			const current = this.messages[index]
			const previous = this.messages[index - 1]
			// 如果时间间隔超过5分钟则显示时间戳
			return current.timestamp - previous.timestamp > 5 * 60 * 1000
		},
		
		formatTime(timestamp) {
			const date = new Date(timestamp)
			const now = new Date()
			
			// 如果是今天，只显示时间
			if (date.toDateString() === now.toDateString()) {
				return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
			}
			
			// 如果是昨天，显示"昨天"
			const yesterday = new Date(now)
			yesterday.setDate(yesterday.getDate() - 1)
			if (date.toDateString() === yesterday.toDateString()) {
				return `昨天 ${date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}`
			}
			
			// 其他情况显示完整日期
			return date.toLocaleString('zh-CN')
		}
	}
}
</script>

<style lang="scss" scoped>
.container {
	display: flex;
	flex-direction: column;
	height: 100vh;
	background-color: #f5f5f5;
}

.message-container {
	flex: 1;
	padding: 20rpx;
	overflow-y: auto;
}

.message-item {
	margin-bottom: 20rpx;
}

.user-message {
	display: flex;
	flex-direction: row-reverse;
	align-items: flex-end;
}

.ai-message {
	display: flex;
	flex-direction: row;
	align-items: flex-end;
}

.avatar {
	width: 80rpx;
	height: 80rpx;
	border-radius: 50%;
	margin: 0 20rpx;
}

.message-bubble {
	max-width: 70%;
	padding: 20rpx;
	border-radius: 10rpx;
	position: relative;
}

.user-bubble {
	background-color: #007AFF;
	color: white;
	margin-left: auto;
}

.ai-bubble {
	background-color: white;
	color: #333;
	margin-right: auto;
}

.message-text {
	font-size: 28rpx;
	line-height: 40rpx;
	word-wrap: break-word;
}

.timestamp {
	text-align: center;
	font-size: 24rpx;
	color: #999;
	margin: 20rpx 0;
}

.input-container {
	background-color: white;
	padding: 20rpx;
	border-top: 1rpx solid #eee;
}

.input-actions {
	display: flex;
	justify-content: space-between;
	margin-bottom: 20rpx;
}

.action-btn {
	font-size: 24rpx;
	padding: 10rpx 20rpx;
	background-color: #f0f0f0;
	border: none;
	border-radius: 8rpx;
}

.input-area {
	display: flex;
	align-items: center;
}

.message-input {
	flex: 1;
	padding: 20rpx;
	border: 1rpx solid #eee;
	border-radius: 10rpx;
	font-size: 28rpx;
	margin-right: 20rpx;
}

.send-btn {
	white-space: nowrap;
	padding: 20rpx 30rpx;
	background-color: #007AFF;
	color: white;
	border: none;
	border-radius: 10rpx;
	font-size: 28rpx;
}
</style>