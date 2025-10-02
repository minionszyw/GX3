<template>
	<view class="container">
		<!-- 用户信息区 -->
		<view class="user-info-section">
			<view class="user-header">
				<image class="user-avatar" :src="userInfo.avatar || '/static/default-avatar.png'" mode="aspectFill"></image>
				<view class="user-details">
					<view class="user-name">{{ userInfo.nickname || '游客' }}</view>
					<button class="edit-btn" @click="editProfile">编辑</button>
				</view>
			</view>
			
			<view class="balance-section">
				<view class="balance-label">账户余额</view>
				<view class="balance-amount">¥{{ (userInfo.tokens / 100).toFixed(2) }}</view>
				<button class="recharge-btn" @click="recharge">充值</button>
			</view>
		</view>
		
		<!-- 菜单区 -->
		<view class="menu-section">
			<view class="menu-item" @click="goToChatHistory">
				<text class="menu-text">聊天记录管理</text>
				<text class="arrow">></text>
			</view>
			
			<view class="menu-item" @click="goToUsageStats">
				<text class="menu-text">使用统计</text>
				<text class="arrow">></text>
			</view>
			
			<view class="menu-item" @click="goToAbout">
				<text class="menu-text">关于我们</text>
				<text class="arrow">></text>
			</view>
		</view>
		
		<!-- 退出登录 -->
		<view class="logout-section">
			<button class="logout-btn" @click="logout">退出登录</button>
		</view>
	</view>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useUserStore } from '@/store/user/user'

export default {
	computed: {
		...mapState(useUserStore, ['userInfo'])
	},
	
	methods: {
		...mapActions(useUserStore, ['logout']),
		
		editProfile() {
			uni.navigateTo({
				url: '/pages/user/edit-profile'
			})
		},
		
		recharge() {
			uni.navigateTo({
				url: '/pages/user/recharge'
			})
		},
		
		goToChatHistory() {
			uni.navigateTo({
				url: '/pages/user/chat-history'
			})
		},
		
		goToUsageStats() {
			uni.navigateTo({
				url: '/pages/user/usage-stats'
			})
		},
		
		goToAbout() {
			uni.navigateTo({
				url: '/pages/about/about'
			})
		},
		
		logout() {
			uni.showModal({
				title: '退出登录',
				content: '确定要退出登录吗？',
				success: (res) => {
					if (res.confirm) {
						this.logout()
						uni.redirectTo({
							url: '/pages/auth/login'
						})
					}
				}
			})
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

.user-info-section {
	background-color: white;
	border-radius: 20rpx;
	padding: 40rpx 30rpx;
	margin-bottom: 20rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.user-header {
	display: flex;
	align-items: center;
	margin-bottom: 40rpx;
}

.user-avatar {
	width: 120rpx;
	height: 120rpx;
	border-radius: 50%;
	margin-right: 30rpx;
}

.user-details {
	flex: 1;
}

.user-name {
	font-size: 36rpx;
	font-weight: bold;
	margin-bottom: 10rpx;
}

.edit-btn {
	font-size: 24rpx;
	padding: 10rpx 20rpx;
	background-color: #f0f0f0;
	border: none;
	border-radius: 8rpx;
}

.balance-section {
	display: flex;
	align-items: center;
	justify-content: space-between;
	background-color: #f8f8f8;
	padding: 30rpx;
	border-radius: 15rpx;
}

.balance-label {
	font-size: 28rpx;
	color: #666;
}

.balance-amount {
	font-size: 40rpx;
	font-weight: bold;
	color: #007AFF;
}

.recharge-btn {
	background-color: #007AFF;
	color: white;
	border: none;
	padding: 15rpx 30rpx;
	border-radius: 10rpx;
	font-size: 28rpx;
}

.menu-section {
	background-color: white;
	border-radius: 20rpx;
	padding: 20rpx 0;
	margin-bottom: 20rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.menu-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 30rpx;
	border-bottom: 1rpx solid #f0f0f0;
}

.menu-item:last-child {
	border-bottom: none;
}

.menu-text {
	font-size: 30rpx;
	color: #333;
}

.arrow {
	font-size: 28rpx;
	color: #999;
}

.logout-section {
	text-align: center;
}

.logout-btn {
	width: 80%;
	background-color: #ff4d4f;
	color: white;
	border: none;
	padding: 25rpx;
	border-radius: 15rpx;
	font-size: 32rpx;
}
</style>