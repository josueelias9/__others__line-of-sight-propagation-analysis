import NextAuth from 'next-auth'
import Credentials from 'next-auth/providers/credentials'
import bcrypt from 'bcrypt'
import postgres from 'postgres'
import { z } from 'zod'
import type { User } from '@/app/lib/types'
import { authConfig } from '@/auth.config'

const sql = postgres(process.env.POSTGRES_URL!, { ssl: false })

async function getUser(email: string): Promise<User | undefined> {
    try {
        const users = await sql<User[]>`SELECT * FROM users WHERE email=${email}`
        return users[0]
    } catch (error) {
        console.error('Failed to fetch user:', error)
        throw new Error('Failed to fetch user.')
    }
}

export const { handlers, auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [
        Credentials({
            async authorize(credentials) {
                const parsedCredentials = z
                    .object({ email: z.string().email(), password: z.string().min(6) })
                    .safeParse(credentials)

                if (parsedCredentials.success) {
                    const { email, password } = parsedCredentials.data

                    const user = await getUser(email)
                    if (!user) return null
                    const temp = await bcrypt.hash(password, 10)
                    console.log('Comparing password with hash:', {
                        password,
                        hash: user.hashed_password,
                        temp
                    })

                    const passwordsMatch = await bcrypt.compare(password, user.hashed_password)
                    if (passwordsMatch) return { id: user.id, email: user.email, name: user.email }
                }

                console.log('Invalid credentials')
                return null
            }
        })
    ]
})
