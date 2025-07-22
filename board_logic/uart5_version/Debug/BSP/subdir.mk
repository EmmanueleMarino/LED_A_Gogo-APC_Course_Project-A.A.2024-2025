################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../BSP/stm32f3_discovery.c \
../BSP/stm32f3_discovery_gyroscope.c 

OBJS += \
./BSP/stm32f3_discovery.o \
./BSP/stm32f3_discovery_gyroscope.o 

C_DEPS += \
./BSP/stm32f3_discovery.d \
./BSP/stm32f3_discovery_gyroscope.d 


# Each subdirectory must supply rules for building sources it contributes
BSP/%.o BSP/%.su BSP/%.cyclo: ../BSP/%.c BSP/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F303xC -c -I../Core/Inc -I../BSP -I../BSP/Components -I../BSP/Components/i3g4250d -I../BSP/Components/l3gd20 -I../BSP/Components/Common -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-BSP

clean-BSP:
	-$(RM) ./BSP/stm32f3_discovery.cyclo ./BSP/stm32f3_discovery.d ./BSP/stm32f3_discovery.o ./BSP/stm32f3_discovery.su ./BSP/stm32f3_discovery_gyroscope.cyclo ./BSP/stm32f3_discovery_gyroscope.d ./BSP/stm32f3_discovery_gyroscope.o ./BSP/stm32f3_discovery_gyroscope.su

.PHONY: clean-BSP

