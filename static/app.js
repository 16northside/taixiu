const { createApp } = Vue;

createApp({
    data() {
        return {
            activeTab: 'home', // Mặc định là trang chủ
            loading: false,
            error: null,
            isAuthenticated: false,
            userInfo: { username: '', email: '', balance: 0 },
            token: localStorage.getItem('token') || '',
            
            // Tabs cho người chưa đăng nhập
            authTabs: [
                { id: 'login', name: 'Đăng nhập', icon: 'fas fa-sign-in-alt' },
                { id: 'register', name: 'Đăng ký', icon: 'fas fa-user-plus' }
            ],
            
            gameTabs: [
                { id: 'home', name: 'Trang chủ', icon: 'fas fa-home' },
                { id: 'taixiu', name: 'Tài Xỉu', icon: 'fas fa-dice' },
                { id: 'bongda', name: 'Bóng Đá', icon: 'fas fa-futbol' },
                { id: 'lode', name: 'Lô Đề', icon: 'fas fa-ticket-alt' }
            ],
            
            // Form data
            loginForm: { username: '', password: '' },
            registerForm: { username: '', email: '', password: '' },
            passwordForm: { old_password: '', new_password: '', confirm_password: '' },
            
            // Error/Success messages
            loginError: '',
            registerError: '',
            registerSuccess: '',
            passwordError: '',
            passwordSuccess: '',
            
            // Game data
            taixiuData: { game: null },
            bongdaData: { matches: [], results: [] },
            lodeData: { numbers: null, history: [] }
        }
    },
    
    mounted() {
        // Kiểm tra token khi app khởi động
        if (this.token) {
            this.isAuthenticated = true;
            this.fetchUserInfo();
        } else {
            // Nếu chưa đăng nhập, chuyển về tab đăng nhập
            this.activeTab = 'login';
        }
        
        // Load dữ liệu game nếu đã đăng nhập
        if (this.isAuthenticated) {
            this.loadData();
        }
        
        // Tự động refresh dữ liệu mỗi 30 giây
        setInterval(() => {
            if (this.isAuthenticated) {
                this.loadData();
            }
        }, 30000);
    },
    
    methods: {
        // Authentication methods
        async login() {
            this.loginError = '';
            this.loading = true;
            
            try {
                const response = await axios.post('http://127.0.0.1:8000/api/users/login/', {
                    username: this.loginForm.username,
                    password: this.loginForm.password
                });
                
                this.token = response.data.access;
                localStorage.setItem('token', this.token);
                this.isAuthenticated = true;
                
                // Lấy thông tin user
                await this.fetchUserInfo();
                
                // Chuyển về trang chủ sau khi đăng nhập
                this.activeTab = 'home';
                
                // Reset form
                this.loginForm = { username: '', password: '' };
                
            } catch (error) {
                console.error('Login error:', error);
                this.loginError = 'Sai tài khoản hoặc mật khẩu!';
            } finally {
                this.loading = false;
            }
        },
        
        async register() {
            this.registerError = '';
            this.registerSuccess = '';
            this.loading = true;
            
            try {
                const response = await axios.post('http://127.0.0.1:8000/api/users/register/', {
                    username: this.registerForm.username,
                    email: this.registerForm.email,
                    password: this.registerForm.password
                });
                
                this.registerSuccess = 'Đăng ký thành công! Bạn có thể đăng nhập.';
                this.registerError = '';
                
                // Reset form
                this.registerForm = { username: '', email: '', password: '' };
                
            } catch (error) {
                console.error('Register error:', error);
                this.registerError = 'Đăng ký thất bại. Tên đăng nhập đã tồn tại hoặc dữ liệu không hợp lệ!';
            } finally {
                this.loading = false;
            }
        },
        
        async fetchUserInfo() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/users/me/', {
                    headers: { Authorization: `Bearer ${this.token}` }
                });
                this.userInfo = response.data;
                this.isAuthenticated = true;
            } catch (error) {
                console.error('Fetch user info error:', error);
                // Token không hợp lệ, logout
                this.logout();
            }
        },
        
        logout() {
            this.token = '';
            localStorage.removeItem('token');
            this.isAuthenticated = false;
            this.userInfo = { username: '', email: '', balance: 0 };
            this.activeTab = 'login';
            
            // Reset tất cả form
            this.loginForm = { username: '', password: '' };
            this.registerForm = { username: '', email: '', password: '' };
            this.passwordForm = { old_password: '', new_password: '', confirm_password: '' };
            
            // Clear messages
            this.loginError = '';
            this.registerError = '';
            this.registerSuccess = '';
            this.passwordError = '';
            this.passwordSuccess = '';
        },
        
        async changePassword() {
            this.passwordError = '';
            this.passwordSuccess = '';
            this.loading = true;
            
            if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
                this.passwordError = 'Mật khẩu mới và xác nhận mật khẩu không khớp!';
                this.loading = false;
                return;
            }
            
            try {
                const response = await axios.post('http://127.0.0.1:8000/api/users/change-password/', {
                    old_password: this.passwordForm.old_password,
                    new_password: this.passwordForm.new_password
                }, {
                    headers: { Authorization: `Bearer ${this.token}` }
                });
                
                this.passwordSuccess = 'Đổi mật khẩu thành công!';
                this.passwordForm = { old_password: '', new_password: '', confirm_password: '' };
                
            } catch (error) {
                console.error('Change password error:', error);
                this.passwordError = 'Đổi mật khẩu thất bại. Vui lòng kiểm tra mật khẩu cũ!';
            } finally {
                this.loading = false;
            }
        },
        
        // Game data methods
        async loadData() {
            this.loading = true;
            this.error = null;
            
            try {
                if (this.activeTab === 'taixiu') {
                    await this.loadTaixiuData();
                } else if (this.activeTab === 'bongda') {
                    await this.loadBongdaData();
                } else if (this.activeTab === 'lode') {
                    await this.loadLodeData();
                }
            } catch (error) {
                console.error('Load data error:', error);
                this.error = 'Không thể tải dữ liệu. Vui lòng thử lại sau.';
            } finally {
                this.loading = false;
            }
        },
        
        async loadTaixiuData() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/taixiu/');
                this.taixiuData = response.data;
            } catch (error) {
                console.error('Load taixiu error:', error);
                this.taixiuData = {
                    message: 'Chào mừng đến với API Tài Xỉu',
                    game: { status: 'Đang chờ', time: '20:00', result: null }
                };
            }
        },
        
        async loadBongdaData() {
            try {
                const [matchesResponse, resultsResponse] = await Promise.all([
                    axios.get('http://127.0.0.1:8000/api/bongda/matches/'),
                    axios.get('http://127.0.0.1:8000/api/bongda/results/')
                ]);
                this.bongdaData.matches = matchesResponse.data.data || [];
                this.bongdaData.results = resultsResponse.data.data || [];
            } catch (error) {
                console.error('Load bongda error:', error);
                this.bongdaData = {
                    matches: [
                        {
                            id: 1, home_team: 'Manchester United', away_team: 'Liverpool',
                            date: '2024-01-15', time: '20:00', status: 'upcoming'
                        }
                    ],
                    results: [
                        {
                            id: 1, home_team: 'Manchester City', away_team: 'Tottenham',
                            home_score: 2, away_score: 1, date: '2024-01-14', status: 'finished'
                        }
                    ]
                };
            }
        },
        
        async loadLodeData() {
            try {
                const [numbersResponse, historyResponse] = await Promise.all([
                    axios.get('http://127.0.0.1:8000/api/lode/numbers/'),
                    axios.get('http://127.0.0.1:8000/api/lode/history/')
                ]);
                this.lodeData.numbers = numbersResponse.data.data || null;
                this.lodeData.history = historyResponse.data.data || [];
            } catch (error) {
                console.error('Load lode error:', error);
                this.lodeData = {
                    numbers: {
                        current_numbers: [12, 34, 56, 78, 90, 23, 45, 67, 89, 1],
                        date: '2024-01-15', region: 'Miền Bắc'
                    },
                    history: [
                        {
                            date: '2024-01-14',
                            numbers: [12, 34, 56, 78, 90, 23, 45, 67, 89, 1],
                            region: 'Miền Bắc'
                        }
                    ]
                };
            }
        },
        
        // Utility methods
        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('vi-VN', {
                day: '2-digit', month: '2-digit', year: 'numeric'
            });
        },
        
        getStatusText(status) {
            const statusMap = {
                'upcoming': 'Sắp diễn ra',
                'live': 'Đang diễn ra',
                'finished': 'Đã kết thúc',
                'cancelled': 'Đã hủy'
            };
            return statusMap[status] || status;
        }
    },
    
    watch: {
        activeTab() {
            if (this.isAuthenticated && ['taixiu', 'bongda', 'lode'].includes(this.activeTab)) {
                this.loadData();
            }
            // Tự động nhúng lại script Minh Ngọc khi chuyển sang tab Lô Đề
            if (this.activeTab === 'lode') {
                this.$nextTick(() => {
                    const box = document.getElementById('box_kqxs_minhngoc');
                    if (box) {
                        box.innerHTML = '';
                        // Xoá các script/link cũ nếu có
                        const oldLink = document.querySelector('link[href="//www.minhngoc.com.vn/style/bangketqua_mini.css"]');
                        if (!oldLink) {
                            const link = document.createElement('link');
                            link.rel = 'stylesheet';
                            link.href = '//www.minhngoc.com.vn/style/bangketqua_mini.css';
                            document.head.appendChild(link);
                        }
                        // jQuery chỉ nhúng nếu chưa có
                        if (!window.jQuery) {
                            const scriptJQ = document.createElement('script');
                            scriptJQ.src = '//www.minhngoc.com.vn/jquery/jquery-1.7.2.js';
                            document.body.appendChild(scriptJQ);
                        }
                        // Config script
                        const configScript = document.createElement('script');
                        configScript.innerHTML = `\n  bgcolor=\"#F2F2F2\";\n  titlecolor=\"#40A9FF\";\n  dbcolor=\"#FB6F92\";\n  fsize=\"14px\";\n  kqwidth=\"340px\";\n`;
                        document.body.appendChild(configScript);
                        // Script kết quả
                        const scriptKQ = document.createElement('script');
                        scriptKQ.src = '//www.minhngoc.com.vn/getkqxs/mien-bac.js';
                        document.body.appendChild(scriptKQ);
                    }
                });
            }
        }
    }
}).mount('#app'); 