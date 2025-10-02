<template>
	<view class="container">
		<view class="search-section">
			<input class="search-input" v-model="searchKeyword" placeholder="搜索聊天记录..." @confirm="searchHistory" />
			<button class="search-btn" @click="searchHistory">搜索</button>
		</view>
		
		<view class="session-list">
			<view 
				v-for="session in filteredSessions" 
				:key="session.id" 
				class="session-item" 
				@click="viewSession(session)"
			>
				<view class="session-info">
					<view class="session-title">{{ session.title }}</view>
					<view class="session-time">{{ formatTime(session.created_at) }}</view>
				</view>
				<view class="session-actions">
					<button class="action-btn delete-btn" @click.stop="deleteSession(session)">删除</button>
				</view>
			</view>
			
			<view v-if="filteredSessions.length === 0" class="empty-tip">
				暂无聊天记录
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
			searchKeyword: ''
		}
	},
	
	computed: {
		...mapState(useChatStore, ['sessions']),
		
		filteredSessions() {
			if (!this.searchKeyword) {
				return this.sessions
			}
			
			return this.sessions.filter(session => 
				session.title.toLowerCase().includes(this.searchKeyword.toLowerCase())
			)
		}
	},
	
	onLoad() {
		// 初始化加载聊天记录
		this.loadSessions()
	},
	
	methods: {
		...mapActions(useChatStore, ['deleteSession']),
		
		async loadSessions() {
			// 模拟加载会话列表
			// 实际项目中这里会调用API获取会话列表
		},
		
		viewSession(session) {
			// 跳转到会话详情页面
			uni.navigateTo({
				url: `/pages/chat/chat?sessionId=${session.id}`
			})
		},
		
		async deleteSession(session) {
			uni.showModal({
				title: '删除会话',
				content: `确定要删除"${session.title}"会话吗？此操作不可恢复。`,
				success: async (res) => {
					if (res.confirm) {
						try {
							await this.deleteSession(session.id)
							uni.showToast({
								title: '删除成功',
								icon: 'success'
							})
						} catch (error) {
							uni.showToast({
								title: '删除失败',
								icon: 'none'
							})
						}
					}
				}
			})
		},
		
		searchHistory() {
			// 搜索功能已在computed中实现
		},
		
		formatTime(timestamp) {
			const date = new Date(timestamp)
			return date.toLocaleDateString('zh-CN')
		}
	}
}
</script>

<style lang="scss" scoped>
.container {
	background-color: #f5f5f5;
	min-height: 100vh;
	padding: 20rpx;
}

.search-section {
	display: flex;
	background-color: white;
	border-radius: 20rpx;
	padding: 20rpx;
	margin-bottom: 20rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.search-input {
	flex: 1;
	padding: 20rpx;
	border: 1rpx solid #eee;
	border-radius: 10rpx;
	font-size: 28rpx;
	margin-right: 20rpx;
}

.search-btn {
	white-space: nowrap;
	padding: 20rpx 30rpx;
	background-color: #007AFF;
	color: white;
	border: none;
	border-radius: 10rpx;
	font-size: 28rpx;
}

.session-list {
	background-color: white;
	border-radius: 20rpx;
	padding: 20rpx 0;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.session-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 30rpx;
	border-bottom: 1rpx solid #f0f0f0;
}

.session-item:last-child {
	border-bottom: none;
}

.session-info {
	flex: 1;
}

.session-title {
	font-size: 30rpx;
	color: #333;
	margin-bottom: 10rpx;
}

.session-time {
	font-size: 24rpx;
	color: #999;
}

.session-actions {
	display: flex;
}

.action-btn {
	font-size: 24rpx;
	padding: 10rpx 20rpx;
	border: none;
	border-radius: 8rpx;
	margin-left: 20rpx;
}

.delete-btn {
	background-color: #ff4d4f;
	color: white;
}

.empty-tip {
	text-align: center;
	padding: 60rpx;
	font-size: 28rpx;
	color: #999;
}
</style>