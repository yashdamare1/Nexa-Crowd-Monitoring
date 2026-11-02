package com.nexa.service;

import com.nexa.entity.Role;
import com.nexa.entity.User;
import com.nexa.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public User registerUser(String name,
                             String email,
                             String password,
                             Role role) {

        if (userRepository.existsByEmail(email)) {
            throw new RuntimeException("Email already registered");
        }

        String encodedPassword = passwordEncoder.encode(password);

        User user = new User(
                name,
                email,
                encodedPassword,
                role
        );

        return userRepository.save(user);
    }
}