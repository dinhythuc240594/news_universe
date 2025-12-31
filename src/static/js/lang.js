
MyLang = {
    
    en: {
        TITLE: 'News - Page News'
        ,NAME_PAGE: 'News'
        ,HOME: 'Home'
        ,NOTIFICATION: 'Notification'
        ,CLOSE: 'Close'
        ,FEATURED_NEWS: 'Featured news'
        ,NO_NEWS: 'No new information available'
        ,LOAD_MORE: 'Load more'
        ,HOT_NEWS: 'Hot news'
        ,NO_HOT_NEWS: 'No breaking news yet.'
        ,WEATHER_HEADER: 'Weather'
        ,LOAD: 'Load...'
        ,LATEST: 'Latest'
        ,INTERNATIONAL: 'International'
        ,PROFILE: 'Profile'
        ,LOGOUT: 'Logout'
        ,MANAGEMENT: 'Management'
        ,SIGN_IN: 'Sign in'
        ,SIGN_UP: 'Sign up'
        ,ABOUT: 'About News'
        ,INTRODUCING: 'Introducing'
        ,CONTACT: 'Contact'
        ,GUIDE: 'Guide'
        ,TERM: 'Term'
        ,SECURITY: 'Security'
        ,SUBCRISE: 'Subcrise'
        ,COPY_RIGHT: '2025 News. All rights reserved.'
        ,SUPPORT: 'Support'
    },
    
    vn: {
        TITLE: 'News - Trang Tin Tức'
        ,NAME_PAGE: 'News'
        ,HOME: 'Trang chủ'
        ,NOTIFICATION: 'Thông báo'
        ,CLOSE: 'Đóng'
        ,FEATURED_NEWS: 'Chưa có tin nổi bật'
        ,NO_NEWS: 'Chưa có tin tức mới'
        ,LOAD_MORE: 'Xem thêm'
        ,HOT_NEWS: 'Xem nhiều'
        ,NO_HOT_NEWS: 'Chưa có tin nóng'
        ,WEATHER_HEADER: 'Thời tiết'
        ,LOAD: 'Đang tải...'
        ,LATEST: 'Mới nhất'
        ,INTERNATIONAL: 'Quốc tế'
        ,PROFILE: 'Thông tin cá nhân'
        ,LOGOUT: 'Đăng xuất'
        ,MANAGEMENT: 'Quản lý'
        ,SIGN_IN: 'Đăng nhập'
        ,SIGN_UP: 'Đăng ký'
        ,ABOUT: 'Về News'
        ,INTRODUCING: 'Giới thiệu'
        ,CONTACT: 'Liên hệ'
        ,GUIDE: 'Hướng dẫn'
        ,TERM: 'Điều khoản'
        ,SECURITY: 'Chính sách bảo mật'
        ,SUBCRISE: 'Theo dõi'
        ,COPY_RIGHT: '2025 News. Tất cả các quyền được bảo lưu.'
        ,SUPPORT: 'Hỗ trợ'
    },
    
    langSite: 'vn',
    
    setSiteLang: function(site){
        langSite = site;
    },
    
    getMsg: function(msg){
        return MyLang[langSite][msg];
    }
    
}