<template>
	<view class="message-item">
		<!-- 用户消息 -->
		<view v-if="message.role === 'user'" class="user-message">
			<view class="message-bubble user-bubble">
				<text class="message-text">{{ message.content }}</text>
			</view>
			<image class="avatar" :src="userAvatar" mode="aspectFill"></image>
		</view>
		
		<!-- AI回复 -->
		<view v-else class="ai-message">
			<image class="avatar" :src="aiAvatar" mode="aspectFill"></image>
			<view class="message-bubble ai-bubble">
				<text class="message-text">{{ message.content }}</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	props: {
		message: {
			type: Object,
			required: true
		},
		userAvatar: {
			type: String,
			default: '/static/user-avatar.png'
		},
		aiAvatar: {
			type: String,
			default: '/static/ai-avatar.png'
		}
	}
}
</script>

<style lang="scss" scoped>
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
</style>