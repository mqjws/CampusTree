export interface AuthorSummary {
  id: number
  alias: string
  avatarEmoji: string
}

export interface PostRecord {
  id: number
  title: string
  summary: string
  content: string
  category: string
  relativeTime: string
  fullTime: string
  likeCount: number
  commentCount: number
  author: AuthorSummary
}

export interface CommentRecord {
  id: number
  content: string
  relativeTime: string
  likeCount: number
  author: AuthorSummary
}

export interface TopicItem {
  id: number
  label: string
  postCount: number
}

export interface CampusNotice {
  id: number
  title: string
  content: string
}

export interface ProfileStats {
  posts: number
  comments: number
  likes: number
}

export interface ProfileRecord {
  userId: string
  nickname: string
  joinedAt: string
  tagline: string
  stats: ProfileStats
}
