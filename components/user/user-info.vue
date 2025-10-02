<template>
	<view class="user-info">
		<image class="user-avatar" :src="userInfo.avatar || '/static/default-avatar.png'" mode="aspectFill"></image>
		<view class="user-details">
			<view class="user-name">{{ userInfo.nickname || '游客' }}</view>
			<view class="user-balance">余额: ¥{{ (userInfo.tokens / 100).toFixed(2) }}</view>
		</view>
	</view>
</template>

<script>
export default {
	props: {
		userInfo: {
			type: Object,
			required: true
		}
	}
}
</script>

<style lang="scss" scoped>
.user-info {
	display: flex;
	align-items: center;
	padding: 30rpx;
	background-color: white;
	border-radius: 20rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
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

.user-balance {
	font-size: 28rpx;
	color: #007AFF;
}
</style>