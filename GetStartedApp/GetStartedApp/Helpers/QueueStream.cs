using System;
using System.Collections.Concurrent;
using System.IO;
using System.Threading;

namespace GetStartedApp.Helpers;
public class QueueStream : Stream
{
    private readonly ConcurrentQueue<byte> _queue = new ConcurrentQueue<byte>();
    private readonly AutoResetEvent _dataAvailable = new AutoResetEvent(false);
    private bool _isCompleted = false;

    // Означува дека продуцентот завршил со пишување податоци во редицата
    public void CompleteAdding()
    {
        _isCompleted = true;
        _dataAvailable.Set(); // Ослободи ги нишките што чекаат
    }

    public override void Write(byte[] buffer, int offset, int count)
    {
        if (_isCompleted) throw new InvalidOperationException("Стримот е означен како завршен.");

        for (int i = 0; i < count; i++)
        {
            _queue.Enqueue(buffer[offset + i]);
        }
        
        _dataAvailable.Set(); // Сигнализирај дека има нови податоци за читање
    }

    public override int Read(byte[] buffer, int offset, int count)
    {
        if (count == 0) return 0;

        // Чекај податоци ако редицата е празна и стримот не е завршен
        while (_queue.IsEmpty && !_isCompleted)
        {
            _dataAvailable.WaitOne();
        }

        int bytesRead = 0;
        while (bytesRead < count && _queue.TryDequeue(out byte b))
        {
            buffer[offset + bytesRead] = b;
            bytesRead++;
        }

        return bytesRead; // Враќа 0 само кога редицата е празна и CompleteAdding() е повикано
    }

    // Задолжителни имплементации за апстрактната класа Stream
    public override bool CanRead => true;
    public override bool CanSeek => false;
    public override bool CanWrite => !_isCompleted;
    public override long Length => _queue.Count;
    public override long Position { get => throw new NotSupportedException(); set => throw new NotSupportedException(); }
    public override void Flush() { }
    public override long Seek(long offset, SeekOrigin origin) => throw new NotSupportedException();
    public override void SetLength(long value) => throw new NotSupportedException();
}
