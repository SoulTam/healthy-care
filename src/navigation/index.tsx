import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#C4704E',
        tabBarInactiveTintColor: '#6B5E54',
        tabBarStyle: { backgroundColor: '#FAF7F2', borderTopColor: '#E8E0D8' },
      }}
    >
      <Tab.Screen name="Home" component={Placeholder} options={{ title: '首页' }} />
      <Tab.Screen name="DietPlan" component={Placeholder} options={{ title: '方案' }} />
      <Tab.Screen name="Community" component={Placeholder} options={{ title: '社区' }} />
      <Tab.Screen name="Profile" component={Placeholder} options={{ title: '我的' }} />
    </Tab.Navigator>
  );
}

function Placeholder() {
  const { View, Text } = require('react-native');
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#FAF7F2' }}>
      <Text style={{ color: '#6B5E54' }}>页面开发中</Text>
    </View>
  );
}

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Main" component={TabNavigator} />
        <Stack.Screen name="Login" component={Placeholder} />
        <Stack.Screen name="Assessment" component={Placeholder} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
