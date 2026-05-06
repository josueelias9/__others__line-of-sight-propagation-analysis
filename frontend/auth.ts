import NextAuth from 'next-auth'
import Google from 'next-auth/providers/google'
import { authConfig } from '@/auth.config'

export const { handlers, signIn, signOut, auth } = NextAuth({
    ...authConfig,
    providers: [Google],
    callbacks: {
        jwt({ token, account }) {
            if (account?.id_token) {
                token.idToken = account.id_token
            }
            return token
        },
        session({ session, token }) {
            session.idToken = token.idToken as string | undefined
            return session
        },
    },
})
