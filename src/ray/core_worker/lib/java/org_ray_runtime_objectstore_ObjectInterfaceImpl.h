/* DO NOT EDIT THIS FILE - it is machine generated */
#include <jni.h>
/* Header for class org_ray_runtime_objectstore_ObjectInterfaceImpl */

#ifndef _Included_org_ray_runtime_objectstore_ObjectInterfaceImpl
#define _Included_org_ray_runtime_objectstore_ObjectInterfaceImpl
#ifdef __cplusplus
extern "C" {
#endif
/*
 * Class:     org_ray_runtime_objectstore_ObjectInterfaceImpl
 * Method:    nativeCreateObjectInterface
 * Signature: (JJLjava/lang/String;)J
 */
JNIEXPORT jlong JNICALL
Java_org_ray_runtime_objectstore_ObjectInterfaceImpl_nativeCreateObjectInterface(
    JNIEnv *, jclass, jlong, jlong, jstring);

/*
 * Class:     org_ray_runtime_objectstore_ObjectInterfaceImpl
 * Method:    nativePut
 * Signature: (JLorg/ray/runtime/objectstore/NativeRayObject;)[B
 */
JNIEXPORT jbyteArray JNICALL
Java_org_ray_runtime_objectstore_ObjectInterfaceImpl_nativePut__JLorg_ray_runtime_objectstore_NativeRayObject_2(
    JNIEnv *, jclass, jlong, jobject);

/*
 * Class:     org_ray_runtime_objectstore_ObjectInterfaceImpl
 * Method:    nativePut
 * Signature: (J[BLorg/ray/runtime/objectstore/NativeRayObject;)V
 */
JNIEXPORT void JNICALL
Java_org_ray_runtime_objectstore_ObjectInterfaceImpl_nativePut__J_3BLorg_ray_runtime_objectstore_NativeRayObject_2(
    JNIEnv *, jclass, jlong, jbyteArray, jobject);

/*
 * Class:     org_ray_runtime_objectstore_ObjectInterfaceImpl
 * Method:    nativeGet
 * Signature: (JLjava/util/List;J)Ljava/util/List;
 */
JNIEXPORT jobject JNICALL Java_org_ray_runtime_objectstore_ObjectInterfaceImpl_nativeGet(
    JNIEnv *, jclass, jlong, jobject, jlong);

/*
 * Class:     org_ray_runtime_objectstore_ObjectInterfaceImpl
 * Method:    nativeWait
 * Signature: (JLjava/util/List;IJ)Ljava/util/List;
 */
JNIEXPORT jobject JNICALL Java_org_ray_runtime_objectstore_ObjectInterfaceImpl_nativeWait(
    JNIEnv *, jclass, jlong, jobject, jint, jlong);

/*
 * Class:     org_ray_runtime_objectstore_ObjectInterfaceImpl
 * Method:    nativeDelete
 * Signature: (JLjava/util/List;ZZ)V
 */
JNIEXPORT void JNICALL Java_org_ray_runtime_objectstore_ObjectInterfaceImpl_nativeDelete(
    JNIEnv *, jclass, jlong, jobject, jboolean, jboolean);

/*
 * Class:     org_ray_runtime_objectstore_ObjectInterfaceImpl
 * Method:    nativeDestroy
 * Signature: (J)V
 */
JNIEXPORT void JNICALL Java_org_ray_runtime_objectstore_ObjectInterfaceImpl_nativeDestroy(
    JNIEnv *, jclass, jlong);

#ifdef __cplusplus
}
#endif
#endif
