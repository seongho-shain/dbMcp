import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export function useAuth() {
  return useContext(AuthContext)
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    setLoading(false)
  }, [])

  const login = async (userData, userType) => {
    try {
      const endpoint = userType === 'teacher' ? '/auth/teacher/login' : '/auth/student/login';
      
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Login response data:', data); // 디버깅용
        console.log('User data from backend:', data.user); // 디버깅용
        
        const userWithType = { ...data.user, user_type: userType };
        console.log('Final user object:', userWithType); // 디버깅용
        
        setUser(userWithType);
        localStorage.setItem('user', JSON.stringify(userWithType));
        return userWithType;
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  const signup = async (userData, userType) => {
    try {
      const endpoint = userType === 'teacher' ? '/auth/teacher/signup' : '/auth/student/signup';
      
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      
      if (response.ok) {
        const data = await response.json();
        const userWithType = { ...data.user, user_type: userType };
        setUser(userWithType);
        localStorage.setItem('user', JSON.stringify(userWithType));
        return userWithType;
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Signup failed');
      }
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  const updateUser = (userData) => {
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const value = {
    user,
    login,
    signup,
    logout,
    updateUser,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}