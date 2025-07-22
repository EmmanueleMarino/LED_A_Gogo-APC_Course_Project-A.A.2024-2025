################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../BSP/Components/i3g4250d/i3g4250d.c 

OBJS += \
./BSP/Components/i3g4250d/i3g4250d.o 

C_DEPS += \
./BSP/Components/i3g4250d/i3g4250d.d 


# Each subdirectory must supply rules for building sources it contributes
BSP/Components/i3g4250d/%.o BSP/Components/i3g4250d/%.su BSP/Components/i3g4250d/%.cyclo: ../BSP/Components/i3g4250d/%.c BSP/Components/i3g4250d/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F303xC -c -I../Core/Inc -I../BSP -I../BSP/Components -I../BSP/Components/i3g4250d -I../BSP/Components/l3gd20 -I../BSP/Components/Common -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-BSP-2f-Components-2f-i3g4250d

clean-BSP-2f-Components-2f-i3g4250d:
	-$(RM) ./BSP/Components/i3g4250d/i3g4250d.cyclo ./BSP/Components/i3g4250d/i3g4250d.d ./BSP/Components/i3g4250d/i3g4250d.o ./BSP/Components/i3g4250d/i3g4250d.su

.PHONY: clean-BSP-2f-Components-2f-i3g4250d

