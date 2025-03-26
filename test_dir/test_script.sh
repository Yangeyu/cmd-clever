#!/bin/bash
# Test script for cmd-clever command execution functionality

# Create some test files
echo "Creating test files..."
mkdir -p test_files
cd test_files

# Create files of different sizes
dd if=/dev/zero of=small.txt bs=1K count=10 2>/dev/null
dd if=/dev/zero of=medium.txt bs=1K count=100 2>/dev/null
dd if=/dev/zero of=large.txt bs=1M count=1 2>/dev/null

# Create some text files with content
echo "Hello, world!" > hello.txt
echo "This is a test file." > test.txt
echo "This file contains important data." > important.txt

# Create a Python file
cat > script.py << 'EOF'
#!/usr/bin/env python
print("Hello from Python!")
for i in range(5):
    print(f"Number: {i}")
EOF

chmod +x script.py

# Create a log file
cat > app.log << 'EOF'
[INFO] 2023-03-25 12:30:45 - Application started
[INFO] 2023-03-25 12:30:46 - Loading configuration
[WARNING] 2023-03-25 12:30:47 - Configuration file not found, using defaults
[INFO] 2023-03-25 12:30:48 - Server started on port 8080
[ERROR] 2023-03-25 12:31:10 - Database connection failed
[INFO] 2023-03-25 12:32:15 - Retrying database connection
[INFO] 2023-03-25 12:32:16 - Database connection successful
EOF

echo "Test files created in $(pwd)"
echo "You can now test cmd-clever with queries like:"
echo "1. 显示当前目录下所有文件的大小"
echo "2. 查找所有的txt文件"
echo "3. 查找app.log文件中的ERROR日志"
echo "4. 运行Python脚本并显示结果"

# Return to original directory
cd .. 