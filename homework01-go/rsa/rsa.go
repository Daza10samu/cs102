package rsa

import (
	"errors"
	"math"
	"math/big"
	"math/rand"
)

type Key struct {
	key int
	n   int
}

type KeyPair struct {
	Private Key
	Public  Key
}

func isPrime(n int) bool {
	if n == 1 {
		return false
	}
	var i int
	i = 2
	for ; i < int(math.Sqrt(float64(n))); i++ {
		if n%i == 0 {
			return false
		}
	}
	return true
}

func gcd(a int, b int) int {
	if b > a {
		a, b = b, a
	}
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

func multiplicativeInverse(e int, phi int) int {
	stack := make([]int, 0)
	a := max(e, phi)
	b := min(e, phi)
	for a%b != 0 {
		stack = append(stack, a/b)
		a, b = b, a%b
	}
	x, y := 0, 1
	for index := len(stack) - 1; index >= 0; index-- {
		x, y = y, x-y*stack[index]
	}
	return (y + phi) % phi
}

func GenerateKeypair(p int, q int) (KeyPair, error) {
	if !isPrime(p) || !isPrime(q) {
		return KeyPair{}, errors.New("Both numbers must be prime.")
	} else if p == q {
		return KeyPair{}, errors.New("p and q can't be equal.")
	}

	// n = pq
	n := p * q

	// phi = (p-1)(q-1)
	phi := (p - 1) * (q - 1)

	e := rand.Intn(phi-1) + 1
	g := gcd(e, phi)
	for g != 1 {
		e = rand.Intn(phi-1) + 1
		g = gcd(e, phi)
	}

	d := multiplicativeInverse(e, phi)
	return KeyPair{Key{e, n}, Key{d, n}}, nil
}

func Encrypt(pk Key, plaintext string) []int {
	cipher := []int{}
	n := new(big.Int)
	for _, ch := range plaintext {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		cipher = append(cipher, int(n.Int64()))
	}
	return cipher
}

func Decrypt(pk Key, cipher []int) string {
	plaintext := ""
	n := new(big.Int)
	for _, ch := range cipher {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		plaintext += string(rune(int(n.Int64())))
	}
	return plaintext
}
