import { defineStore } from 'pinia'
import apiClient from '@/utils/api'

export const useChatStore = defineStore('chat', {
	state: () => ({
		sessions: [], // 会话列表
		currentSession: null, // 当前会话
		messages: [], // 消息列表
		isLoading: false, // 加载状态
		error: null // 错误信息
	}),
	
	actions: {
		// 创建新会话
		async createSession() {
			try {
				// 实际API调用
				const sessionData = await apiClient.post('/sessions', {
					title: '新会话'
				})
				
				this.sessions.push(sessionData)
				this.currentSession = sessionData
				this.messages = []
				return sessionData
			} catch (error) {
				this.error = error.message
				throw error
			}
		},
		
		// 发送消息
		async sendMessage(content) {
			try {
				this.isLoading = true
				
				// 添加用户消息到本地
				const userMessage = {
					id: Date.now(),
					session_id: this.currentSession.id,
					content: content,
					role: 'user',
					timestamp: new Date().getTime()
				}
				this.messages.push(userMessage)
				
				// 实际API调用获取AI回复
				const aiMessage = await apiClient.post(`/sessions/${this.currentSession.id}/messages`, {
					content: content,
					role: 'user'
				})
				
				// 模拟计费：根据消息长度计算token消耗
				const tokenCost = Math.ceil(content.length / 4) + Math.ceil(aiMessage.content.length / 4)
				
				this.messages.push(aiMessage)
				return aiMessage
			} catch (error) {
				this.error = error.message
				throw error
			} finally {
				this.isLoading = false
			}
		},
		
		// 获取历史记录
		async fetchHistory(sessionId) {
			try {
				// 实际API调用
				const messages = await apiClient.get(`/sessions/${sessionId}/messages`)
				
				this.messages = messages
			} catch (error) {
				this.error = error.message
				throw error
			}
		},
		
		// 清空消息
		clearMessages() {
			this.messages = []
		},
		
		// 删除会话
		async deleteSession(sessionId) {
			try {
				// 实际API调用
				await apiClient.delete(`/sessions/${sessionId}`)
				
				this.sessions = this.sessions.filter(session => session.id !== sessionId)
				
				if (this.currentSession && this.currentSession.id === sessionId) {
					this.currentSession = null
					this.messages = []
				}
			} catch (error) {
				this.error = error.message
				throw error
			}
		}
	}
})