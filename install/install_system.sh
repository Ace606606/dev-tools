# apt update && apt install -y \
# 	build-essential cmake git gdb lldb \
# 	clang clang-format clang-tidy cppcheck \
# 	ninja-build pkg-config make \
# 	bash-completion curl wget openssh-client \
# 	python3 python3-pip python3-venv\
# 	protobuf-compiler protobuf-compiler-grpc \
# 	libprotobuf-dev libgrpc++-dev libgrpc-dev libprotoc-dev \
# 	doxygen graphviz valgrind shfmt \
# 	docker.io docker-compose

apt update && apt install -y \
	build-essential cmake git gdb lldb \
	clang clang-format clang-tidy cppcheck \
	pkg-config make \
	bash-completion curl wget openssh-client \
	#shfmt valgrind \
	libprotobuf-dev libgrpc++-dev libgrpc-dev libprotoc-dev

# python3 -m venv .venv
# source ./.venv/bin/activate
# pip install grpcio grpcio-tools protobuf mypy-protobuf mypy black
