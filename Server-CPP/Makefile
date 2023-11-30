BUILD_DEFAULT=debug

BUILD_DIR=build
SRC_DIR=src
INCLUDE_DIR=include
TEST_DIR=test

TARGET_NAME=server
TARGET=$(BUILD_DIR)/$(TARGET_NAME)

# Shell Commands
CC=g++
CXX=g++
AR=ar rcs
MKDIR=mkdir -p
RM=rm -rf
CP=cp

# useful utility to convert lowercase to uppercase. 
UPPERCASE_CMD = tr '[:lower:][\-/]' '[:upper:][__]'

# Flags for compiler and other programs
CFLAGS=-Wall -Wextra -Werror
VALG_FLAGS = --leak-check=full --track-origins=yes
DEBUG_FLAGS = -g -DDEBUG
RELEASE_FLAGS = -march=native 
LINKER_FLAGS =

# Color codes for print statements
GREEN = \033[1;32m
CYAN = \033[1;36m
RED = \033[1;31m
RESET = \033[0m

# Verbosity control. Inspired from the Contiki-NG build system. A few hacks here and there, will probably improve later.
ifeq ($(V),1)
  TRACE_CC =
  TRACE_LD =
  TRACE_MKDIR =
  TRACE_CP =
	TRACE_AR =
	TRACE_RUN =
  Q ?=
  
  BUILD_SUCCESS=
  BUILD_FAILURE=:
  LINK_FAILURE=:
  INIT_SUCCESS=
  INIT_MAIN=
  RUN=
  VALGRIND_RUN=
  
  CLEAN=
  MK_INIT_ERROR=
else

  TRACE_CC       = @echo "$(CYAN)   CC     $(RESET)" $<
  TRACE_LD       = @echo "$(CYAN)   LD     $(RESET)" $@
	TRACE_AR 		   = @echo "$(CYAN)   AR     $(RESET)" $@
  TRACE_MKDIR    = @echo "$(CYAN)   MKDIR  $(RESET)" $@
  TRACE_CP       = @echo "$(CYAN)   CP     $(RESET)" $< "-->" $@
	TRACE_RUN      = @echo "$(GREEN)   RUN    $(RESET)" $<
  Q ?= @
  
  BUILD_SUCCESS  =@echo "   --      $(GREEN)Build successful in $(BUILD_DEFAULT) mode.$(RESET)"
  BUILD_FAILURE  =echo  "   --      $(RED)Build failed.$(RESET)"; exit 1
  LINK_FAILURE   =echo  "   --      $(RED)Linking failed.$(RESET)"; exit 1
  INIT_MAIN      =@echo "   --      $(CYAN)Creating main.c$(RESET)"
  INIT_SUCCESS   =@echo "   --      $(GREEN)Initialized the project structure$(RESET)"
  RUN            =@echo "   --      $(CYAN)Executing$(RESET): $(TARGET_NAME)"
  VALGRIND_RUN   =@echo "   --      $(CYAN)Running Valgrind on$(RESET): $(TARGET_NAME)"
  CLEAN          =@echo "   --      $(GREEN)Cleaned$(RESET): $(BUILD_DIR)/*"
  
  MK_INIT_ERROR  =@echo "$(RED)Error: $(SRC_DIR) directory doesn't exist. Please run make init to initialize the project.$(RESET)"
endif

# Sets flags based on the build mode.
ifeq ($(BUILD_DEFAULT), release)
  CFLAGS += $(RELEASE_FLAGS)
else
  CFLAGS += $(DEBUG_FLAGS)
endif

# Find all the source files and corresponding objects
SRCS := $(wildcard $(SRC_DIR)/*.cpp)
OBJS := $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SRCS))

SRC_DIR_EXISTS := $(shell if [ -d "$(SRC_DIR)" ]; then echo 1; else echo 0; fi)

# The TARGET target depends on the generated object files. 
$(TARGET): $(OBJS)
	$(TRACE_LD)
	$(Q) $(CC) $(CFLAGS) -I$(INCLUDE_DIR) $^ -o $@ $(LINKER_FLAGS) || ($(LINK_FAILURE))
	$(BUILD_SUCCESS)

# The object files' targets, depend on their corresponding source files.
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(TRACE_CC)
	$(Q) $(CC) $(CFLAGS) -I$(INCLUDE_DIR) -c $< -o $@ || ($(BUILD_FAILURE))

# Create the build, src and include directories if they don't exist.
$(BUILD_DIR) $(SRC_DIR) $(INCLUDE_DIR):
	$(TRACE_MKDIR)
	$(Q) $(MKDIR) $@
# Initializes the project directories, and creates a main.c file in the src directory.
init: $(BUILD_DIR) $(SRC_DIR) $(INCLUDE_DIR)
	$(INIT_SUCCESS)

# Checks if src directory exists. If it doesn't, probably they haven't run `make init` yet.
ifeq ($(SRC_DIR_EXISTS), 0)
run: 
	$(MK_INIT_ERROR)
else
run: $(TARGET)
	$(RUN)
	$(Q) $(TARGET)
endif

all: $(TARGET) 
	$(BUILD_SUCCESS)

# Runs the program in valgrind, for debugging purposes (if needed)
valgrind: $(TARGET)
	$(VALGRIND_RUN)
	$(Q) valgrind $(VALG_FLAGS) $(TARGET)

clean: 
	$(CLEAN)
	$(Q) $(RM) $(BUILD_DIR)/*