import NextAuth from 'next-auth'
import Credentials from 'next-auth/providers/credentials'
import { authConfig } from '@/auth.config'

const BACKEND_URL = process.env.BACKEND_URL ?? 'http://localhost:8000'

export const { handlers, signIn, signOut, auth } = NextAuth({
    ...authConfig,
    trustHost: true,
    providers: [
        Credentials({
            credentials: {
                email: { label: 'Email', type: 'email' },
                password: { label: 'Password', type: 'password' },
            },
            async authorize(credentials) {
                if (!credentials?.email || !credentials?.password) return null

                const formData = new URLSearchParams()
                formData.append('username', credentials.email as string)
                formData.append('password', credentials.password as string)

                let res: Response
                try {
                    res = await fetch(`${BACKEND_URL}/api/login/access-token`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: formData.toString(),
                    })
                } catch {
                    return null
                }

                if (!res.ok) return null

                const { access_token } = (await res.json()) as { access_token: string }
                return {
                    id: credentials.email as string,
                    email: credentials.email as string,
                    accessToken: access_token,
                }
            },
        }),
    ],
    callbacks: {
        jwt({ token, user }) {
            if (user && 'accessToken' in user) {
                token.accessToken = user.accessToken as string
            }
            return token
        },
        session({ session, token }) {
            session.accessToken = token.accessToken as string | undefined
            return session
        },
    },
})
