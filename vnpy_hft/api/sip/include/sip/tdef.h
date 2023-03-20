
#ifndef _DATATYPE_DEFINE_H_
#define _DATATYPE_DEFINE_H_
// �ӿ�ʹ�õĹ�������ͽṹ
// tdef.h LINUX��/Windows�����
// ver 1.0
// ����: ��� ��̩����֤ȯ 2013/10/23 

// LINUX�� GCC���ͳ���(�ֽ�)
// type         x86_sizeof(type)    x64_sizeof(type)
// char         1                   1
// short        2                   2
// int          4                   4
// long         4                   8
// void*        4                   8
// long long    8                   8
// float        4                   4
// double       8                   8

//__GNUC__
//linux
//__i386__  ��x86
//__x86_64__  ��X64


//windows VC������
// type         x86_sizeof(type)    x64_sizeof(type)
// char         1                   1
// short        2                   2
// int          4                   4
// long         4                   4
// void*        4                   8
// long long    8                   8
// float        4                   4
// double       8                   8

//_WIN32
//	Defined for applications for Win32 and Win64. Always defined.
//_WIN64
//	Defined for applications for Win64.
//_WINDOWS_ ��Windows.h�ж����#ifndef _WINDOWS_
//#define _WINDOWS_





// ������������
typedef char				T_I8;
typedef unsigned char		T_U8;

typedef short int			T_I16;
typedef unsigned short int	T_U16;

typedef int					T_I32;
typedef unsigned int		T_U32;

typedef long long			T_I64;
typedef unsigned long long	T_U64;

typedef float				T_F32;
typedef double				T_F64;

#ifdef linux    // linux
    #define UNALIGNED
    #define __stdcall

    typedef	long			    T_HANDLE;	// so�ӿ��õľ��������ָ�����ͻ�ת
    typedef long			    T_PARAM;	// ���ڻص�����������ָ�����ͻ�ת

    //{{ windowsϰ�ߵĶ���
    typedef int                 SOCKET;

    #define FALSE               0
    #define TRUE                1
    #define BOOL                bool

    #define INVALID_SOCKET      (-1)
    #define SOCKET_ERROR        (-1)
    #define INVALID_HANDLE_FILE (-1)
    #define stricmp(a,b)        strcasecmp(a,b)
    //}}
#else // windows
    #ifdef _WIN64
        typedef long long           T_HANDLE;
        typedef long long			T_PARAM;	// ���ڻص�����������ָ�����ͻ�ת
    #else
        typedef	long			    T_HANDLE;
        typedef long			    T_PARAM;	// ���ڻص�����������ָ�����ͻ�ת
    #endif //WIN64
#endif



#endif // _DATATYPE_DEFINE_H_
