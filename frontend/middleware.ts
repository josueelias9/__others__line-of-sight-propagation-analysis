import NextAuth from 'next-auth'
import { authConfig } from '@/auth.config'

export const { auth: middleware } = NextAuth(authConfig)

export const config = {
    // Include /login so authorized() can redirect logged-in users away from it
    matcher: ['/((?!api/auth|_next/static|_next/image|favicon\.ico).*)']
}
