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

            if (isOnSeed) return true

            if (isOnLogin) {
                // Already authenticated → send to home
                if (isLoggedIn) return Response.redirect(new URL('/', nextUrl))
                return true
            }

            // All other routes require auth
            return isLoggedIn
        }
    }
} satisfies NextAuthConfig
