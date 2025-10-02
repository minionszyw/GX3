<template>
	<view class="container">
		<view class="logo-section">
			<image class="logo" src="/static/logo.png" mode="aspectFit"></image>
			<view class="app-title">国学大师</view>
			<view class="app-subtitle">传承千年智慧，解答人生疑惑</view>
		</view>
		
		<view class="login-section">
			<view class="login-tabs">
				<view 
					class="tab-item" 
					:class="{ active: activeTab === 'wechat' }"
					@click="switchTab('wechat')"
				>
					微信登录
				</view>
				<view 
					class="tab-item" 
					:class="{ active: activeTab === 'email' }"
					@click="switchTab('email')"
				>
					邮箱登录
				</view>
			</view>
			
			<view class="login-form" v-if="activeTab === 'email'">
				<view class="form-item">
					<input 
						class="form-input" 
						v-model="email" 
						placeholder="请输入邮箱" 
						type="email" 
						@confirm="login"
					/>
				</view>
				
				<view class="form-item">
					<input 
						class="form-input" 
						v-model="password" 
						placeholder="请输入密码" 
						type="password" 
						@confirm="login"
					/>
				</view>
				
				<button class="login-btn" @click="login" :disabled="!canLogin">登录</button>
				
				<view class="form-footer">
					<navigator class="link" url="/pages/auth/register">还没有账号？立即注册</navigator>
				</view>
			</view>
			
			<view class="wechat-login" v-else>
				<button class="wechat-login-btn" @click="wechatLogin">
					<image class="wechat-icon" src="/static/wechat-icon.png" mode="aspectFit"></image>
					微信一键登录
				</button>
				
				<view class="agreement">
					登录即表示您同意
					<navigator class="link" url="/pages/auth/agreement">用户协议</navigator>
					和
					<navigator class="link" url="/pages/auth/privacy">隐私政策</navigator>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import { mapActions } from 'pinia'
import { useUserStore } from '@/store/user/user'

export default {
	data() {
		return {
			activeTab: 'wechat', // 默认微信登录
			email: '',
			password: ''
		}
	},
	
	computed: {
		canLogin() {
			return this.email && this.password
		}
	},
	
	methods: {
		...mapActions(useUserStore, ['loginWithWechat', 'loginWithEmail']),
		
		switchTab(tab) {
			this.activeTab = tab
		},
		
		async wechatLogin() {
			try {
				// 调用用户store的微信登录方法
				await this.loginWithWechat()
				
				uni.showToast({
					title: '登录成功',
					icon: 'success'
				})
				
				// 跳转到首页
				setTimeout(() => {
					uni.switchTab({
						url: '/pages/chat/chat'
					})
				}, 1000)
			} catch (error) {
				uni.showToast({
					title: '登录失败',
					icon: 'none'
				})
			}
		},
		
		async login() {
			if (!this.canLogin) return
			
			try {
				const credentials = {
					email: this.email,
					password: this.password
				}
				
				// 调用用户store的邮箱登录方法
				await this.loginWithEmail(credentials)
				
				uni.showToast({
					title: '登录成功',
					icon: 'success'
				})
				
				// 跳转到首页
				setTimeout(() => {
					uni.switchTab({
						url: '/pages/chat/chat'
					})
				}, 1000)
			} catch (error) {
				uni.showToast({
					title: '登录失败',
					icon: 'none'
				})
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.container {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	min-height: 100vh;
	padding: 20rpx;
}

.logo-section {
	text-align: center;
	padding: 100rpx 0 60rpx;
}

.logo {
	width: 160rpx;
	height: 160rpx;
	margin-bottom: 30rpx;
}

.app-title {
	font-size: 48rpx;
	color: white;
	font-weight: bold;
	margin-bottom: 20rpx;
}

.app-subtitle {
	font-size: 28rpx;
	color: rgba(255, 255, 255, 0.8);
}

.login-section {
	background-color: white;
	border-radius: 20rpx;
	padding: 40rpx;
	box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.2);
}

.login-tabs {
	display: flex;
	margin-bottom: 40rpx;
}

.tab-item {
	flex: 1;
	text-align: center;
	padding: 20rpx;
	font-size: 32rpx;
	color: #999;
	border-bottom: 2rpx solid #f0f0f0;
}

.tab-item.active {
	color: #007AFF;
	border-bottom: 2rpx solid #007AFF;
}

.form-item {
	margin-bottom: 30rpx;
}

.form-input {
	width: 100%;
	padding: 25rpx;
	border: 1rpx solid #eee;
	border-radius: 10rpx;
	font-size: 28rpx;
	box-sizing: border-box;
}

.login-btn {
	width: 100%;
	background-color: #007AFF;
	color: white;
	border: none;
	padding: 25rpx;
	border-radius: 10rpx;
	font-size: 32rpx;
	margin-top: 20rpx;
}

.login-btn:disabled {
	background-color: #ccc;
}

.form-footer {
	text-align: center;
	margin-top: 30rpx;
}

.wechat-login-btn {
	width: 100%;
	background-color: #07c160;
	color: white;
	border: none;
	padding: 25rpx;
	border-radius: 10rpx;
	font-size: 32rpx;
	display: flex;
	align-items: center;
	justify-content: center;
}

.wechat-icon {
	width: 50rpx;
	height: 50rpx;
	margin-right: 20rpx;
}

.agreement {
	text-align: center;
	font-size: 24rpx;
	color: #999;
	margin-top: 30rpx;
	line-height: 1.5;
}

.link {
	color: #007AFF;
	display: inline;
}

.link:hover {
	text-decoration: underline;
}
</style>