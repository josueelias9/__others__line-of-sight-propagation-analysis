import type { NextAuthConfig } from 'next-auth'

export const authConfig = {
    trustHost: true,
    pages: {
        signIn: '/login'
    },
    providers: [],
    callbacks: {
        authorized({ auth, request: { nextUrl } }) {
            const isLoggedIn = !!auth?.user
            const isOnLogin = nextUrl.pathname === '/login'
            const isOnSeed = nextUrl.pathname === '/seed'
            const isOnHome = nextUrl.pathname === '/'
            const isOnAnalyzer = nextUrl.pathname.startsWith('/analyzer')

            if (isOnAnalyzer) {
                if (isLoggedIn) {
                    return true
                }
                return false
            }
            return true
        }
    }
} satisfies NextAuthConfig
